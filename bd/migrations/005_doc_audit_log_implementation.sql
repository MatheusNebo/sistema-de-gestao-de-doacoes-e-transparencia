-- Migration 005: Documentação do sistema de auditoria
-- Data: 03/06/2026
-- Descrição: Sistema de rastreamento de alterações implementado

-- SISTEMA DE AUDITORIA COMPLETO:

-- 1. TABELA: audit_log
--    - Registra TODAS as alterações em entidades críticas
--    - Campos: user_id, entity_type, entity_id, action (CREATE/UPDATE/DELETE), old_value (JSON), new_value (JSON)
--    - Índices: entity (rápido por entity_type+entity_id), user (rápido por user_id), timestamp (histórico recente)

-- 2. MODELS AUDITADOS:
--    ✅ beneficiary (CREATE, UPDATE, DELETE)
--    ✅ donor (CREATE, UPDATE, DELETE)
--    ✅ product (CREATE, UPDATE, DELETE)
--    ⏳ donation (próximo)
--    ⏳ distribution (próximo)
--    ⏳ inventory (próximo)

-- 3. ENDPOINTS DE CONSULTA:
--    GET /audits/ - últimos 100 registros
--    GET /audits/entity/{entity_type}/{entity_id} - histórico completo de uma entidade
--    GET /audits/user/{user_id} - últimas ações de um usuário

-- 4. CARACTERÍSTICAS:
--    - Timestamps automáticos (CURRENT_TIMESTAMP)
--    - JSON para armazenar valores antigos/novos (flexível para futuras alterações)
--    - user_id nullable (ações do sistema não precisam de usuário)
--    - Passwords removidas automaticamente (não auditamos senhas)
--    - Transactions garantem atomicidade

-- 5. PRÓXIMAS MELHORIAS:
--    - Adicionar auditoria em donation, distribution, inventory
--    - Implementar filtro de data/período
--    - Criar dashboard de auditoria
--    - Soft deletes com campos audit

-- SEM MUDANÇAS ESTRUTURAIS NECESSÁRIAS - Sistema totalmente implementado em app/services/audit_service.py
