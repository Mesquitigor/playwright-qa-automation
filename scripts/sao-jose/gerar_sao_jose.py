#!/usr/bin/env python3
"""
Script para construção de imagem simbólica de São José.

Representa a paternidade e a masculinidade viril do Patrono da Igreja Católica
e Pai da Família de Nazaré — sem necessariamente mostrar rostos.

Uso:
    python gerar_sao_jose.py                          # gera com Pillow (local)
    python gerar_sao_jose.py --tema oficina           # variação temática
    python gerar_sao_jose.py --api openai             # usa DALL-E (requer OPENAI_API_KEY)
    python gerar_sao_jose.py --listar-temas           # lista variações disponíveis
    python gerar_sao_jose.py --apenas-prompt          # imprime o prompt sem gerar
"""

from __future__ import annotations

import argparse
import os
import sys
import textwrap
from datetime import datetime
from pathlib import Path

from prompts import (
    NEGATIVE_PROMPT,
    NEGATIVE_PROMPT_EN,
    PROMPT_PRINCIPAL,
    PROMPT_PRINCIPAL_EN,
    VARIACOES,
)

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "output"


def montar_prompt(tema: str | None = None, idioma: str = "pt") -> tuple[str, str]:
    """Monta prompt principal + variação temática."""
    if idioma == "en":
        base = PROMPT_PRINCIPAL_EN
        neg = NEGATIVE_PROMPT_EN
    else:
        base = PROMPT_PRINCIPAL
        neg = NEGATIVE_PROMPT

    if tema:
        if tema not in VARIACOES:
            disponiveis = ", ".join(VARIACOES.keys())
            raise ValueError(f"Tema '{tema}' não encontrado. Disponíveis: {disponiveis}")
        extra = VARIACOES[tema]["prompt_extra"]
        prompt = f"{base}\n\nVARIAÇÃO — {VARIACOES[tema]['nome']}:\n{extra}"
    else:
        prompt = base

    return prompt, neg


def gerar_com_pillow(caminho: Path, tema: str | None = None) -> Path:
    """
    Gera composição simbólica local com Pillow.
    Representação estilizada: mãos, ferramentas, luz dourada — sem rostos.
    """
    try:
        from PIL import Image, ImageDraw, ImageFilter, ImageFont
    except ImportError:
        print("Instale Pillow: pip install Pillow")
        sys.exit(1)

    largura, altura = 1024, 1280
    img = Image.new("RGB", (largura, altura), "#1a1208")
    draw = ImageDraw.Draw(img)

    # Fundo: gradiente terroso (simula luz de oficina)
    for y in range(altura):
        ratio = y / altura
        r = int(26 + ratio * 60)
        g = int(18 + ratio * 40)
        b = int(8 + ratio * 20)
        draw.line([(0, y), (largura, y)], fill=(r, g, b))

    # Janela com luz dourada (lado direito superior)
    luz = Image.new("RGB", (largura, altura), "#000000")
    luz_draw = ImageDraw.Draw(luz)
    luz_draw.polygon(
        [(largura - 280, 80), (largura - 60, 80), (largura - 60, 320), (largura - 380, 380)],
        fill="#c9a227",
    )
    luz = luz.filter(ImageFilter.GaussianBlur(radius=80))
    img = Image.blend(img, luz, alpha=0.35)

    draw = ImageDraw.Draw(img)

    # Bancada de madeira
    draw.rectangle([(0, 780), (largura, 920)], fill="#5c3d1e")
    draw.rectangle([(0, 920), (largura, altura)], fill="#3d2810")

    # Tábua de madeira em perspectiva
    draw.polygon(
        [(120, 720), (largura - 100, 680), (largura - 80, 780), (100, 820)],
        fill="#8b6914",
        outline="#6b4f0a",
    )

    # Veios da madeira
    for i in range(8):
        x = 140 + i * 100
        draw.line([(x, 730), (x + 40, 810)], fill="#7a5c10", width=2)

    # Mãos estilizadas (retângulos arredondados — sugestão, não realismo)
    cor_pele = "#c4956a"
    # Mão esquerda segurando madeira
    draw.ellipse([(180, 640), (320, 760)], fill=cor_pele, outline="#a07050", width=3)
    # Mão direita com ferramenta
    draw.ellipse([(400, 620), (540, 740)], fill=cor_pele, outline="#a07050", width=3)

    # Braços (sugestão de força)
    draw.polygon([(200, 760), (280, 500), (340, 500), (320, 760)], fill="#6b4423")
    draw.polygon([(460, 740), (520, 480), (580, 480), (540, 740)], fill="#6b4423")

    # Túnica (ombros e costas — figura de costas)
    draw.polygon(
        [(250, 500), (largura // 2 + 80, 420), (largura // 2 + 200, 500), (largura // 2 + 180, 780), (200, 780)],
        fill="#4a3728",
        outline="#3a2a1e",
    )
    # Avental de couro
    draw.rectangle(
        [(largura // 2 - 20, 500), (largura // 2 + 120, 750)],
        fill="#5c3a1a",
        outline="#4a2e10",
    )

    # Cinzel (ferramenta)
    draw.polygon([(520, 600), (560, 580), (570, 700), (530, 710)], fill="#888888")
    draw.rectangle([(555, 580), (575, 620)], fill="#654321")

    # Plaina
    draw.rectangle([(700, 750), (900, 790)], fill="#4a3520", outline="#3a2810")
    draw.rectangle([(880, 740), (920, 800)], fill="#666666")

    # Lírio branco (canto inferior esquerdo)
    draw.ellipse([(60, 830), (100, 870)], fill="#f5f0e0")  # vaso
    for angulo in range(-30, 40, 20):
        import math
        cx, cy = 80, 820
        for petala in range(3):
            px = cx + int(25 * math.cos(math.radians(angulo + petala * 40)))
            py = cy - 30 - petala * 8
            draw.ellipse([(px - 8, py - 15), (px + 8, py + 5)], fill="#ffffff", outline="#e8e8e8")

    # Sandálias infantis na parede
    for sx in (750, 820):
        draw.ellipse([(sx, 200), (sx + 50, 240)], fill="#8b5a2b", outline="#6b4020")
        draw.line([(sx + 10, 220), (sx + 40, 220)], fill="#5c3a1a", width=2)

    # Serragem / partículas de luz
    import random
    random.seed(42)
    for _ in range(120):
        x = random.randint(100, largura - 100)
        y = random.randint(200, 800)
        size = random.randint(1, 3)
        draw.ellipse([(x, y), (x + size, y + size)], fill="#d4a84b")

    # Título discreto
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 28)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
        font_small = font

    titulo = "São José — Pai da Família de Nazaré"
    subtitulo = VARIACOES[tema]["nome"] if tema else "O Trabalhador e o Guardião"

    draw.text((largura // 2, 60), titulo, fill="#d4a84b", font=font, anchor="mm")
    draw.text((largura // 2, 100), subtitulo, fill="#a08050", font=font_small, anchor="mm")

    caminho.parent.mkdir(parents=True, exist_ok=True)
    img.save(caminho, quality=95)
    return caminho


def gerar_com_openai(prompt: str, caminho: Path, tamanho: str = "1024x1792") -> Path:
    """Gera imagem via API OpenAI DALL-E 3."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Erro: defina a variável de ambiente OPENAI_API_KEY.")
        sys.exit(1)

    try:
        from openai import OpenAI
    except ImportError:
        print("Instale o SDK: pip install openai")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    print("Gerando imagem com DALL-E 3 (pode levar alguns segundos)...")
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt[:4000],
        size=tamanho,
        quality="hd",
        style="natural",
        n=1,
    )

    import urllib.request

    url = response.data[0].url
    caminho.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, caminho)
    return caminho


def salvar_prompt(caminho: Path, prompt: str, negativo: str) -> None:
    """Salva prompt em arquivo de texto para uso em outras ferramentas."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    conteudo = textwrap.dedent(f"""\
        # Prompt — São José (gerado em {datetime.now().isoformat()})

        ## Prompt positivo
        {prompt}

        ## Prompt negativo
        {negativo}
    """)
    caminho.write_text(conteudo, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Constrói imagem simbólica de São José — paternidade e masculinidade viril do trabalhador.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Exemplos:
              python gerar_sao_jose.py
              python gerar_sao_jose.py --tema caminho --api openai
              python gerar_sao_jose.py --apenas-prompt --tema noite
        """),
    )
    parser.add_argument(
        "--tema",
        choices=list(VARIACOES.keys()),
        help="Variação temática da composição",
    )
    parser.add_argument(
        "--api",
        choices=["local", "openai"],
        default="local",
        help="Backend de geração (padrão: local com Pillow)",
    )
    parser.add_argument(
        "--idioma",
        choices=["pt", "en"],
        default="pt",
        help="Idioma do prompt (para API OpenAI)",
    )
    parser.add_argument(
        "--saida",
        type=Path,
        help="Caminho do arquivo de saída (padrão: output/sao_jose_<timestamp>.png)",
    )
    parser.add_argument(
        "--apenas-prompt",
        action="store_true",
        help="Apenas exibe/salva o prompt, sem gerar imagem",
    )
    parser.add_argument(
        "--listar-temas",
        action="store_true",
        help="Lista variações temáticas disponíveis",
    )

    args = parser.parse_args()

    if args.listar_temas:
        print("\nVariações temáticas disponíveis:\n")
        for chave, dados in VARIACOES.items():
            print(f"  {chave:12} — {dados['nome']}")
        print()
        return

    prompt, negativo = montar_prompt(args.tema, args.idioma)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sufixo = f"_{args.tema}" if args.tema else ""
    caminho_saida = args.saida or OUTPUT_DIR / f"sao_jose{sufixo}_{timestamp}.png"
    caminho_prompt = caminho_saida.with_suffix(".txt")

    if args.apenas_prompt:
        print("\n=== PROMPT POSITIVO ===\n")
        print(prompt)
        print("\n=== PROMPT NEGATIVO ===\n")
        print(negativo)
        salvar_prompt(caminho_prompt, prompt, negativo)
        print(f"\nPrompt salvo em: {caminho_prompt}")
        return

    salvar_prompt(caminho_prompt, prompt, negativo)
    print(f"Prompt salvo em: {caminho_prompt}")

    if args.api == "openai":
        caminho = gerar_com_openai(prompt, caminho_saida)
    else:
        print("Gerando composição simbólica local...")
        caminho = gerar_com_pillow(caminho_saida, args.tema)

    print(f"\nImagem gerada: {caminho}")
    print("\nSão José, rogai por nós.")


if __name__ == "__main__":
    main()
