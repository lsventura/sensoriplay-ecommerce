-- Script de carga inicial para o e-commerce Sensori Play
-- Rode ESTE arquivo depois de aplicar db/schema.sql

-- Usuário administrador padrão (ajuste o hash de senha antes de usar em produção)
INSERT INTO users (name, email, password_hash, is_admin)
VALUES ('Administrador', 'admin@sensoriplay.com.br', 'CHANGE_ME_HASH', TRUE)
ON CONFLICT (email) DO NOTHING;

-- Produtos iniciais
INSERT INTO products (name, description, price, category, age_range, emoji, badge, featured, stock)
VALUES
('Cubo Sensorial Fidget', 'Cubo multi-textura com diferentes estímulos táteis', 45.90, 'sensorial', '3-5', '🎲', 'Novo', TRUE, 20),
('Quebra-Cabeça 3D Animais', 'Quebra-cabeça tridimensional para desenvolvimento cognitivo', 62.90, 'cognitivo', '6-8', '🦁', 'Destaque', TRUE, 15),
('Spinner Tátil Premium', 'Spinner com diferentes texturas para alívio de ansiedade', 38.90, 'sensorial', '6-8', '🌀', NULL, TRUE, 30),
('Torre de Empilhar Colorida', 'Desenvolve coordenação motora e reconhecimento de cores', 54.90, 'motor', '0-2', '🏗️', 'Mais Vendido', TRUE, 25),
('Kit Formas Geométricas', 'Conjunto de formas para aprendizado de geometria', 49.90, 'cognitivo', '3-5', '🔷', NULL, TRUE, 40),
('Bola Sensorial Texturizada', 'Bola com relevos para estimulação sensorial', 42.90, 'sensorial', '0-2', '⚽', 'Novo', TRUE, 35)
ON CONFLICT DO NOTHING;

-- Cupons iniciais
INSERT INTO coupons (code, description, discount_percent, discount_value, is_free_shipping, min_order_value, active)
VALUES
('SENSORI10', '10% OFF em qualquer compra', 10.00, NULL, FALSE, 0, TRUE),
('BEMVINDO', 'R$ 20,00 de desconto para primeira compra', NULL, 20.00, FALSE, 80.00, TRUE),
('FRETEGRATIS', 'Frete grátis acima de R$ 150,00', NULL, NULL, TRUE, 150.00, TRUE)
ON CONFLICT (code) DO NOTHING;
