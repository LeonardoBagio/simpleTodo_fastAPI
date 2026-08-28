"""Dados canônicos dos cadastros globais (Status e Categoria).

Cores aproximadas da paleta do Notion (2ª e 3ª imagens). A migration que
popula o banco real carrega uma cópia estática destes mesmos valores; aqui
ficam disponíveis para os testes (que criam o schema via metadata, sem rodar
migrations).
"""

CATALOG_STATUSES = [
    {'code': 'nao_iniciada', 'label': 'Não iniciada', 'color': '#9b9a97', 'group': 'a_fazer', 'sort_order': 1},  # noqa: E501
    {'code': 'stand_by', 'label': 'Stand by', 'color': '#cb7e3a', 'group': 'a_fazer', 'sort_order': 2},  # noqa: E501
    {'code': 'aguardando_retorno', 'label': 'Aguardando retorno', 'color': '#dfab01', 'group': 'a_fazer', 'sort_order': 3},  # noqa: E501
    {'code': 'code_review', 'label': 'Code-review', 'color': '#e03e3e', 'group': 'em_andamento', 'sort_order': 4},  # noqa: E501
    {'code': 'em_andamento', 'label': 'Em andamento', 'color': '#337ea9', 'group': 'em_andamento', 'sort_order': 5},  # noqa: E501
    {'code': 'pronto_para_homologar', 'label': 'Pronto para homologar', 'color': '#c1558b', 'group': 'em_andamento', 'sort_order': 6},  # noqa: E501
    {'code': 'homologacao', 'label': 'Homologação', 'color': '#9065b0', 'group': 'em_andamento', 'sort_order': 7},  # noqa: E501
    {'code': 'concluido', 'label': 'Concluído', 'color': '#448361', 'group': 'concluidos', 'sort_order': 8},  # noqa: E501
]

CATALOG_CATEGORIES = [
    {'code': 'hotfix', 'label': 'hotfix', 'color': '#b8496b', 'sort_order': 1},
    {'code': 'feature', 'label': 'feature', 'color': '#337ea9', 'sort_order': 2},  # noqa: E501
    {'code': 'data_conversion', 'label': 'data conversion', 'color': '#c1912e', 'sort_order': 3},  # noqa: E501
    {'code': 'release', 'label': 'Release', 'color': '#448361', 'sort_order': 4},  # noqa: E501
    {'code': 'task', 'label': 'Task', 'color': '#9065b0', 'sort_order': 5},
    {'code': 'epic', 'label': 'Epic', 'color': '#c1558b', 'sort_order': 6},
    {'code': 'sub_issue', 'label': 'sub issue', 'color': '#8a6ea6', 'sort_order': 7},  # noqa: E501
    {'code': 'orientacao', 'label': 'Orientação', 'color': '#9b9a97', 'sort_order': 8},  # noqa: E501
]
