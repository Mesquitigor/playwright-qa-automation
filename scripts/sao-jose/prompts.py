"""
Prompts simbólicos para imagem de São José — Pai da Família de Nazaré.
Foco: paternidade, masculinidade viril do trabalhador, sem rostos visíveis.
"""

# Cena principal: oficina de carpinteiro em Nazaré, luz dourada do entardecer
PROMPT_PRINCIPAL = """
Uma pintura sacra em estilo renascentista contemporâneo, atmosfera reverente e calorosa.

CENA: Oficina de carpinteiro em Nazaré, século I. Um homem robusto e trabalhador — São José —
visto de costas ou em três quartos, rosto oculto pela sombra ou pelo ângulo. Mãos largas,
calejadas e fortes seguram um cinzel e um pedaço de madeira de oliveira. O corpo transmite
força serena, disciplina e proteção paterna.

ELEMENTOS SIMBÓLICOS:
- Ferramentas de carpinteiro: serra, plaina, martelo, esquadro de madeira
- Lascas de madeira e serragem no chão de pedra
- Um pequeno banco de madeira infantil ao fundo (sugestão de presença do Menino)
- Sandálias pequenas de couro penduradas na parede
- Um lírio branco em vaso de barro (pureza e obediência)
- Luz dourada entrando por janela baixa, como luz divina suave
- Túnica simples de linho e avental de couro gasto pelo trabalho
- Braços musculosos mas não exagerados — força de quem trabalha com dignidade

ATMOSFERA: masculinidade viril sem agressividade; paternidade protetora; silêncio operoso;
santidade encontrada no trabalho honesto. Nenhum rosto humano claramente visível.
Não mostrar o rosto de Jesus nem de Maria — apenas sugestões indiretas da família.

ESTILO: óleo sobre tela, pinceladas visíveis, paleta terrosa (ocre, sépia, dourado, verde-oliva),
iluminação chiaroscuro suave. Composição vertical, adequada para devoção.
""".strip()

PROMPT_PRINCIPAL_EN = """
A sacred painting in contemporary Renaissance style, reverent and warm atmosphere.

SCENE: Carpenter's workshop in Nazareth, 1st century. A robust working man — Saint Joseph —
seen from behind or three-quarter view, face hidden by shadow or angle. Broad, calloused,
strong hands hold a chisel and a piece of olive wood. His body conveys serene strength,
discipline, and fatherly protection.

SYMBOLIC ELEMENTS:
- Carpenter's tools: saw, plane, hammer, wooden square
- Wood shavings and sawdust on stone floor
- A small child's wooden stool in the background (suggestion of the Child's presence)
- Small leather sandals hanging on the wall
- A white lily in a clay pot (purity and obedience)
- Golden light entering through a low window, like soft divine light
- Simple linen tunic and leather apron worn by honest labor
- Muscular arms but not exaggerated — strength of dignified work

ATMOSPHERE: virile masculinity without aggression; protective fatherhood; operative silence;
holiness found in honest labor. No human face clearly visible.
Do not show the face of Jesus or Mary — only indirect suggestions of the family.

STYLE: oil on canvas, visible brushstrokes, earthy palette (ochre, sepia, gold, olive green),
soft chiaroscuro lighting. Vertical composition, suitable for devotion.
""".strip()

# Variações temáticas
VARIACOES = {
    "oficina": {
        "nome": "O Trabalhador de Nazaré",
        "prompt_extra": (
            "Foco nas mãos de São José entalhando madeira. "
            "Gotas de suor na testa oculta. Pó de serragem flutuando na luz."
        ),
    },
    "caminho": {
        "nome": "O Protetor no Caminho",
        "prompt_extra": (
            "São José visto de costas caminhando por estrada de pedra ao entardecer, "
            "bordão de madeira na mão direita, mochila de couro nas costas. "
            "À frente, apenas a silhueta pequena de uma criança de mãos dadas com uma mulher "
            "(rostos não visíveis, vistos de costas). Céu alaranjado e protetor."
        ),
    },
    "noite": {
        "nome": "O Guardião da Noite",
        "prompt_extra": (
            "Interior humilde à noite, lamparina de óleo acesa. "
            "São José sentado de perfil, rosto na penumbra, vigiando em oração silenciosa. "
            "Ferramentas repousam ordenadamente. Sensação de vigília paterna e vigília espiritual."
        ),
    },
    "flores": {
        "nome": "Lírio e Madeira",
        "prompt_extra": (
            "Composição ainda: mãos masculinas entrelaçadas em oração sobre bancada de madeira, "
            "com lírio branco e esquadro de carpinteiro. Simbolismo da virgindade e do trabalho."
        ),
    },
}

NEGATIVE_PROMPT = """
rosto visível, face detalhada, retrato frontal, caricatura, cartoon, anime,
violência, sangue, armas, sensualidade, nudez, feminização, corpo frágil,
modernidade, eletricidade, máquinas industriais, texto, watermark, assinatura,
baixa qualidade, borrado, distorção, membros extras, anatomia incorreta
""".strip()

NEGATIVE_PROMPT_EN = """
visible face, detailed face, frontal portrait, caricature, cartoon, anime,
violence, blood, weapons, sensuality, nudity, effeminization, fragile body,
modernity, electricity, industrial machines, text, watermark, signature,
low quality, blurry, distortion, extra limbs, incorrect anatomy
""".strip()
