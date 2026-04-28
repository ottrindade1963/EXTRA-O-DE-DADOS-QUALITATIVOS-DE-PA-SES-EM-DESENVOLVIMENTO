"""Pipeline da análise exploratória completa."""

from eda_loader import carregar_dados, resumo_geral
from eda_visualizacoes import (
    plot_missing,
    plot_histogramas,
    plot_boxplots,
    plot_correlacao,
    plot_evolucao_temporal,
    plot_top_paises,
    plot_scatter_pib_industria,
    plot_violin_emprego,
    plot_pairplot,
    plot_heatmap_paises,
)


def executar_eda():
    """Executa a análise exploratória completa."""
    print("=" * 50)
    print("  ANÁLISE EXPLORATÓRIA — PAÍSES EMERGENTES")
    print("=" * 50)

    df = carregar_dados()
    resumo_geral(df)

    plot_missing(df)
    plot_histogramas(df)
    plot_boxplots(df)
    plot_correlacao(df)
    plot_evolucao_temporal(df)
    plot_top_paises(df)
    plot_scatter_pib_industria(df)
    plot_violin_emprego(df)
    plot_pairplot(df)
    plot_heatmap_paises(df)

    print("\n" + "=" * 50)
    print("  ✅ ANÁLISE CONCLUÍDA — 10 gráficos gerados!")
    print(f"  📂 Resultados em: resultados_eda/")
    print("=" * 50)
