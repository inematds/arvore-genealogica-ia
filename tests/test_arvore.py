"""Testes do scripts/arvore.py. Rodar: python3 -m unittest discover tests"""
import os
import subprocess
import sys
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(AQUI, "..", "scripts", "arvore.py")
MODELO = os.path.join(AQUI, "..", "modelos", "pessoas.csv")


def rodar(*args):
    return subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True)


def csv_tmp(texto):
    f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8")
    f.write("id,nome,nascimento,local_nascimento,pai_id,mae_id,fonte,status,nota\n" + texto)
    f.close()
    return f.name


class TestArvore(unittest.TestCase):
    def test_modelo_gera_html(self):
        with tempfile.TemporaryDirectory() as d:
            saida = os.path.join(d, "a.html")
            r = rodar(MODELO, "--saida", saida)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("3 confirmados", r.stdout)  # p07 sem fonte foi rebaixado
            t = open(saida, encoding="utf-8").read()
            self.assertIn("mermaid@11.4.1", t)
            self.assertIn("Giuseppe Rossi", t)

    def test_confirmado_sem_fonte_vira_hipotese(self):
        r = rodar(csv_tmp("p1,Fulano,1900,,,,,CONFIRMADO,\n"), "--mermaid")
        self.assertEqual(r.returncode, 0)
        self.assertIn("sem fonte", r.stderr)
        self.assertIn("class p1 hip", r.stdout)

    def test_fonte_generica_vira_hipotese(self):
        r = rodar(csv_tmp("p1,A,1900,,,,https://www.familysearch.org/,CONFIRMADO,\n"
                          "p2,B,1900,,,,link do registro aqui,CONFIRMADO,\n"
                          "p3,C,1900,,,,https://www.familysearch.org/ark:/61903/1:1:XXXX,CONFIRMADO,\n"), "--mermaid")
        self.assertIn("class p1 hip", r.stdout)
        self.assertIn("class p2 hip", r.stdout)
        self.assertIn("class p3 conf", r.stdout)

    def test_fonte_legitima_com_here_nao_rebaixa(self):
        r = rodar(csv_tmp("p1,A,1900,,,,\"Ellis Island manifest, original here at home\",CONFIRMADO,\n"
                          "p2,B,1900,,,,certidão do cartório Cole,CONFIRMADO,\n"), "--mermaid")
        self.assertIn("class p1 conf", r.stdout)
        self.assertIn("class p2 conf", r.stdout)

    def test_tabela_em_ingles(self):
        modelo = os.path.join(AQUI, "..", "modelos", "people.csv")
        with tempfile.TemporaryDirectory() as d:
            saida = os.path.join(d, "a.html")
            r = rodar(modelo, "--output", saida)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("3 confirmed, 5 hypotheses, 2 warnings", r.stdout)
            self.assertIn("without a source", r.stderr)
            t = open(saida, encoding="utf-8").read()
            self.assertIn('lang="en"', t)
            self.assertIn("(hypothesis)", t)

    def test_tabela_em_espanhol(self):
        modelo = os.path.join(AQUI, "..", "modelos", "personas.csv")
        r = rodar(modelo, "--mermaid")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("desconocido", r.stderr)  # HIPÓTESIS com acento é aceito
        self.assertIn("sin fuente", r.stderr)
        self.assertIn("(hipótesis)", r.stdout)
        self.assertIn("class p04 conf", r.stdout)

    def test_cerca_do_chat_e_ponto_e_virgula(self):
        f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8")
        f.write("```csv\nid;nombre;nacimiento;lugar_nacimiento;padre_id;madre_id;fuente;estado;nota\n"
                "p1;Ana;1900;;;;acta 12;CONFIRMADO;\n```\n"); f.close()
        r = rodar(f.name, "--mermaid")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("class p1 conf", r.stdout)

    def test_cabecalho_desconhecido_avisa_em_tres_linguas(self):
        f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False)
        f.write("a,b\n1,2\n"); f.close()
        r = rodar(f.name, "--mermaid")
        self.assertNotEqual(r.returncode, 0)
        for s in ("faltam colunas", "missing columns", "faltan columnas"):
            self.assertIn(s, r.stderr)

    def test_csv_do_excel_cp1252_e_fonte_nao_ha(self):
        f = tempfile.NamedTemporaryFile("wb", suffix=".csv", delete=False)
        f.write("id;nome;nascimento;local_nascimento;pai_id;mae_id;fonte;status;nota\r\n"
                "p1;João;1900;;;;certidão;CONFIRMADO;\r\np2;Zé;1900;;;;não há;CONFIRMADO;\r\n".encode("cp1252")); f.close()
        r = rodar(f.name, "--mermaid")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("class p1 conf", r.stdout)
        self.assertIn("class p2 hip", r.stdout)

    def test_idade_impossivel_avisa(self):
        r = rodar(csv_tmp("p1,Filho,1900,,p2,,x,CONFIRMADO,\np2,Pai,1895,,,,x,CONFIRMADO,\n"), "--mermaid")
        self.assertIn("teria 5 anos", r.stderr)

    def test_pai_inexistente_avisa(self):
        r = rodar(csv_tmp("p1,Filho,1900,,p9,,x,CONFIRMADO,\n"), "--mermaid")
        self.assertIn("'p9' não existe", r.stderr)

    def test_so_confirmados_esconde_hipotese(self):
        r = rodar(csv_tmp("p1,Real,1900,,,,x,CONFIRMADO,\np2,Inventado,1870,,,,,HIPOTESE,\n"),
                  "--mermaid", "--so-confirmados")
        self.assertIn("Real", r.stdout)
        self.assertNotIn("Inventado", r.stdout)

    def test_elo_sem_prova_e_tracejado(self):
        r = rodar(csv_tmp("p1,Filho,1900,,p2,,x,CONFIRMADO,\np2,Pai,1870,,,,,HIPOTESE,\n"), "--mermaid")
        self.assertIn("p2 -.-> p1", r.stdout)

    def test_id_repetido_falha(self):
        r = rodar(csv_tmp("p1,A,,,,,,,\np1,B,,,,,,,\n"), "--mermaid")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("id repetido", r.stderr)

    def test_coluna_faltando_falha(self):
        f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False)
        f.write("id,nome\np1,A\n"); f.close()
        r = rodar(f.name, "--mermaid")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("faltam colunas", r.stderr)


if __name__ == "__main__":
    unittest.main()
