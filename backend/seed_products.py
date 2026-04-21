"""
seed_products.py — Popula o DB com 18 produtos reais do catálogo SensoriPlay + cupom BEMVINDO10.
Idempotente: usa UPSERT por nome do produto.
Execução: python3 backend/seed_products.py (a partir da raiz do projeto)
"""
import os
import sys
from datetime import datetime
from pathlib import Path

# Garante que imports do projeto funcionem a partir de qualquer diretório
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "backend"))

# O DB está na raiz do projeto
DB_PATH = ROOT / "sensoriplay.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"
os.environ.setdefault("DATABASE_URL", DATABASE_URL)

import database  # noqa: E402

# ── Cria tabelas se não existirem ──────────────────────────────────────────
if database.engine is None:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    database.engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    database.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=database.engine)

database.Base.metadata.create_all(bind=database.engine)

# ── Dados dos 18 produtos (fonte: RESEARCH.md §5) ─────────────────────────
PRODUCTS = [
    dict(
        name="Tapete Sensorial Squish de Apertar — Foco e Autorregulação",
        description=(
            "Desenvolvido para a janela de 3+ anos, quando a criança começa a buscar "
            "autorregulação pelo toque. Os painéis de gel apertável ativam receptores "
            "táteis nas mãos e dedos, favorecendo foco e calma em momentos de sobrecarga sensorial. "
            "Material: silicone atóxico BPA-free, lavável. Útil para crianças com TEA, TDAH ou "
            "desenvolvimento típico que buscam regulação sensorial."
        ),
        price=39.90,
        category="Fidget",
        age_range="3+",
        emoji="🟣",
        badge="Mais vendido",
        featured=True,
        stock=50,
    ),
    dict(
        name="Kit 5 Discos Sensoriais Táteis — Exploração Pés e Mãos",
        description=(
            "Cinco discos com texturas distintas (pontas, relevos, nervuras, malha, lisa) para "
            "exploração tátil de pés e mãos. Cada disco trabalha receptores cutâneos diferentes, "
            "estimulando integração sensorial e propriocepção plantar — base para equilíbrio e "
            "coordenação motora. Indicado para 1+ ano. Material: borracha EVA atóxica."
        ),
        price=89.90,
        category="Tato",
        age_range="1+",
        emoji="🔵",
        badge="Staff pick",
        featured=True,
        stock=30,
    ),
    dict(
        name="Abafador Infantil de Ruído 25dB — Conforto Sensorial",
        description=(
            "Projetado para crianças com hipersensibilidade auditiva, o abafador reduz ruídos "
            "em até 25dB sem eliminar a comunicação. Estrutura ajustável em 3+ anos, acolchoamento "
            "interno macio, dobradiças silenciosas. Certificado CE. Indicado para ambientes com "
            "sobrecarga sonora: festas, shows, transporte público, escola."
        ),
        price=279.90,
        category="Abafador",
        age_range="3+",
        emoji="🎧",
        badge="Recomendado por OTs",
        featured=True,
        stock=20,
    ),
    dict(
        name="Colar Mordedor Sensorial em Silicone Alimentar",
        description=(
            "Para crianças que buscam estimulação oral como forma de regulação sensorial. "
            "Fabricado em silicone grau alimentício, livre de BPA, ftalatos e látex. "
            "Design discreto de colar para uso no dia a dia e na escola. "
            "Resiste à mordida contínua sem perder forma. Lavável em água e sabão. "
            "Útil para crianças com TDAH, TEA e hipossensibilidade oral."
        ),
        price=72.90,
        category="Mastigável",
        age_range="2+",
        emoji="🔴",
        badge=None,
        featured=False,
        stock=40,
    ),
    dict(
        name="Luminária Retroprojetora de Estrelas — Calma Visual",
        description=(
            "Projeta constelações e nebulosas no teto e paredes com rotação lenta e silenciosa. "
            "Estímulo visual suave que favorece regulação emocional e transição para o sono — "
            "indicado como recurso de sala calma ou rotina noturna. "
            "3 modos de cor (azul, verde, vermelho), timer automático de 30 min. "
            "Bivolt, bivolt, USB. Para crianças 3+."
        ),
        price=199.90,
        category="Luminoso",
        age_range="3+",
        emoji="⭐",
        badge="Novidade",
        featured=True,
        stock=25,
    ),
    dict(
        name="Pau de Chuva Cristal 50cm — Experiência Auditiva Calmante",
        description=(
            "Instrumento de percussão suave com sementes naturais que reproduz o som de chuva ao "
            "ser virado. O som previsível e rítmico favorece atenção sustentada e regulação "
            "emocional em crianças com hipersensibilidade auditiva. Corpo transparente permite "
            "acompanhar visualmente o movimento das sementes — duplo estímulo. Para 2+ anos."
        ),
        price=164.90,
        category="Musical",
        age_range="2+",
        emoji="🌧️",
        badge=None,
        featured=False,
        stock=15,
    ),
    dict(
        name="Almofada Ponderada 1.5kg — Apoio à Autorregulação",
        description=(
            "A pressão distribuída uniformemente sobre o colo ativa o sistema nervoso "
            "parassimpático, favorecendo calma e foco. Peso recomendado: 10% do peso corporal "
            "(indicada para crianças de 12-18kg). Preenchimento com microesferas de vidro, "
            "capa removível e lavável. Baseada em princípios de integração sensorial de Ayres (1972). "
            "Útil para TEA, TDAH e ansiedade infantil."
        ),
        price=149.00,
        category="Ponderado",
        age_range="4+",
        emoji="🔶",
        badge="Recomendado por OTs",
        featured=True,
        stock=20,
    ),
    dict(
        name="Cobertor Ponderado Infantil 3kg (100x130cm)",
        description=(
            "A pressão profunda distribuída pelo cobertor simula o abraço — recurso de regulação "
            "sensorial amplamente utilizado por terapeutas ocupacionais. Peso: 3kg, dimensões: "
            "100x130cm. Preenchimento com microesferas de vidro costuradas em bolsos individuais "
            "para distribuição uniforme. Tecido externo: algodão 400 fios, hipoalergênico. "
            "Lavável em máquina (carga delicada). Para crianças 6+ anos."
        ),
        price=349.90,
        category="Ponderado",
        age_range="6+",
        emoji="🛏️",
        badge="Mais vendido",
        featured=True,
        stock=10,
    ),
    dict(
        name="Kit Fidget Spinner + Cubo + Pop-it — Caixa Ansiedade",
        description=(
            "Três ferramentas de regulação sensorial portáteis para uso discreto em sala de "
            "aula ou ambientes com alto estímulo. O spinner trabalha foco motor, o cubo oferece "
            "6 tipos de estímulo tátil, o pop-it trabalha repetição rítmica e autorregulação. "
            "Materiais: silicone e ABS atóxicos. Para crianças 5+ anos."
        ),
        price=59.90,
        category="Fidget",
        age_range="5+",
        emoji="🌀",
        badge=None,
        featured=False,
        stock=60,
    ),
    dict(
        name="Balanço Sensorial de Tecido — Estimulação Vestibular",
        description=(
            "O balanço é o recurso de estimulação vestibular mais potente disponível para uso "
            "doméstico. O movimento de balanço ativa o sistema vestibular — responsável pelo "
            "equilíbrio e orientação espacial — e tem efeito regulador documentado em crianças "
            "com TEA e TDAH. Tecido: nylon ripstop 210kg de resistência. Inclui kit de fixação "
            "no teto. Capacidade: 80kg. Para crianças 3+ anos."
        ),
        price=389.00,
        category="Vestibular",
        age_range="3+",
        emoji="🪢",
        badge="Profissional",
        featured=True,
        stock=8,
    ),
    dict(
        name="Caixa Sensorial de Areia + Letras Texturizadas",
        description=(
            "A areia cinética oferece estimulação tátil rica ao mesmo tempo que proporciona "
            "atividade de alfabetização: as letras texturizadas são enterradas e descobertas, "
            "associando forma tátil e grafema. Método inspirado no ensino Montessori. "
            "Areia atóxica e não alergênica, moldável e não-pegajosa. "
            "Ideal para crianças em fase de pré-alfabetização (4+ anos)."
        ),
        price=129.90,
        category="Alfabetização",
        age_range="4+",
        emoji="🏖️",
        badge=None,
        featured=False,
        stock=25,
    ),
    dict(
        name="Bolas de Gel Anti-Stress (Kit 6 Texturas)",
        description=(
            "Seis bolas com texturas e resistências diferentes (suave, nervurada, espinhosa, "
            "lisa, reticulada, com relevos) para exploração tátil graduada. A compressão trabalha "
            "propriocepção manual e fortalecimento muscular dos dedos — base para motricidade fina. "
            "Material: silicone e gel atóxico. Para crianças 3+ anos."
        ),
        price=74.90,
        category="Tato",
        age_range="3+",
        emoji="🟢",
        badge=None,
        featured=False,
        stock=35,
    ),
    dict(
        name="Fantoche Bocão Sensorial — Comunicação e Faz de Conta",
        description=(
            "Fantoche de boca articulada com pelagem de diferentes texturas (lisa, felpuda, "
            "áspera) que combina estimulação tátil com desenvolvimento de comunicação e jogo "
            "simbólico. O personagem pode 'comer' pequenos objetos — recurso utilizado em "
            "terapia de linguagem para crianças com TEA. Lavável em máquina. Para 3+ anos."
        ),
        price=119.00,
        category="Linguagem",
        age_range="3+",
        emoji="🧸",
        badge=None,
        featured=False,
        stock=20,
    ),
    dict(
        name="Chocalho Mordedor de Silicone para Bebê",
        description=(
            "Na janela de 0 a 12 meses, o bebê explora o mundo com as mãos e a boca. "
            "Este chocalho combina estimulação auditiva (som suave ao agitar) com exploração "
            "oral e tátil. Silicone grau alimentício, livre de BPA e ftalatos. "
            "Alças de diferentes espessuras trabalham preensão palmar e pinça. "
            "Certificado INMETRO. Lavável em dishwasher."
        ),
        price=45.90,
        category="Bebê",
        age_range="0-12m",
        emoji="🍼",
        badge="Selo INMETRO",
        featured=True,
        stock=45,
    ),
    dict(
        name="Mesa de Água Sensorial Montessori",
        description=(
            "A água é um dos materiais sensoriais mais ricos e acessíveis. Esta mesa com altura "
            "adaptada para 2+ anos inclui acessórios de transferência (conchas, colheres, "
            "potes medidores) que trabalham coordenação motora fina, noção de volume e "
            "exploração tátil/temperatura. Inspirada no método Montessori de livre exploração. "
            "Material: plástico PP atóxico, desmontável para limpeza."
        ),
        price=299.90,
        category="Água/Banho",
        age_range="2+",
        emoji="💧",
        badge=None,
        featured=False,
        stock=12,
    ),
    dict(
        name="Massinha Therapy Putty Resistência Média (4 potes)",
        description=(
            "Massinha terapêutica de grau clínico para fortalecimento de mãos e dedos. "
            "Resistência média (equivalente ao código roxo em terapia ocupacional). "
            "4 potes de 85g em cores distintas. Material: silicone terapêutico, não-tóxico, "
            "não-alergênico. Não resseca. Usada em consultórios de TO para desenvolvimento "
            "de motricidade fina, preensão e regulação sensorial oral. Para 4+ anos."
        ),
        price=89.90,
        category="Motricidade",
        age_range="4+",
        emoji="🎨",
        badge="Profissional",
        featured=False,
        stock=30,
    ),
    dict(
        name="Quebra-Cabeça Sensorial de Madeira — Texturas e Cores",
        description=(
            "Quebra-cabeça de 12 peças em madeira certificada FSC com superfícies de diferentes "
            "texturas (lisa, serrilhada, ondulada, pontilhada). Cada peça é grande o suficiente "
            "para manipulação por crianças 3+. Trabalha coordenação olho-mão, reconhecimento de "
            "formas e discriminação tátil simultaneamente. Tinta atóxica certificada. "
            "Bom para TEA e desenvolvimento típico."
        ),
        price=159.90,
        category="Cognição",
        age_range="3+",
        emoji="🧩",
        badge=None,
        featured=True,
        stock=18,
    ),
    dict(
        name="Kit Sala Calma Essencial — Abafador + Almofada + Luminária + 3 Fidgets",
        description=(
            "O kit completo para montar uma estação de regulação sensorial em casa ou no consultório. "
            "Inclui: abafador infantil 25dB, almofada ponderada 1.5kg, luminária de estrelas, "
            "e 3 fidgets curados (spinner, cubo de estímulo, pop-it). "
            "Economia de R$121 vs compra individual. "
            "Indicado por terapeutas ocupacionais como kit de primeiro recurso para famílias "
            "em início de acompanhamento. Todos os itens vêm em caixa com guia de uso."
        ),
        price=649.00,
        category="Bundle",
        age_range="3-10",
        emoji="🎁",
        badge="Bundle — economia R$121",
        featured=True,
        stock=5,
    ),
]

# ── Cupom ─────────────────────────────────────────────────────────────────
COUPON = dict(
    code="BEMVINDO10",
    description="Cupom de boas-vindas: 10% de desconto na primeira compra acima de R$100",
    discount_percent=10.0,
    discount_value=None,
    is_free_shipping=False,
    min_order_value=100.00,
    active=True,
    expires_at=None,
)

# ── Inserção idempotente ───────────────────────────────────────────────────
def seed():
    db = database.SessionLocal()
    now = datetime.utcnow()
    inserted = updated = 0

    try:
        for data in PRODUCTS:
            existing = db.query(database.Product).filter(
                database.Product.name == data["name"]
            ).first()

            if existing:
                for k, v in data.items():
                    setattr(existing, k, v)
                existing.updated_at = now
                updated += 1
            else:
                product = database.Product(
                    **data,
                    created_at=now,
                    updated_at=now,
                )
                db.add(product)
                inserted += 1

        # Cupom BEMVINDO10
        existing_coupon = db.query(database.Coupon).filter(
            database.Coupon.code == COUPON["code"]
        ).first()

        if not existing_coupon:
            coupon = database.Coupon(
                code=COUPON["code"],
                description=COUPON["description"],
                discount_percent=COUPON["discount_percent"],
                discount_value=COUPON["discount_value"],
                is_free_shipping=COUPON["is_free_shipping"],
                min_order_value=COUPON["min_order_value"],
                active=COUPON["active"],
                expires_at=COUPON["expires_at"],
                created_at=now,
            )
            db.add(coupon)
            print(f"  Cupom BEMVINDO10 criado.")
        else:
            print(f"  Cupom BEMVINDO10 ja existe — ignorado.")

        db.commit()
        print(f"Seed concluido: {inserted} produtos inseridos, {updated} atualizados.")

    except Exception as e:
        db.rollback()
        print(f"ERRO no seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print(f"DB: {DB_PATH}")
    seed()
