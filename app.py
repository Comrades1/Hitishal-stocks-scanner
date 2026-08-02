# --- 2. SECTOR MOMENTUM RANKING (PROPORTIONAL SCALING -10 TO +10) ---
    sector_summary = df_data.groupby('Sector').agg(
        Avg_Change=('Change %', 'mean'),
        Bullish_Count=('Change %', lambda x: (x > 0).sum()),
        Total_Count=('Symbol', 'count')
    ).reset_index()

    # Raw Score Calculation
    sector_summary['Raw_Score'] = sector_summary['Avg_Change'] * (sector_summary['Bullish_Count'] / sector_summary['Total_Count'])

    # Dynamic Scaling Logic: Maps max score to 10 and min score to -10 without flattening top performers
    max_val = sector_summary['Raw_Score'].abs().max()
    if max_val > 0:
        sector_summary['Strength Score'] = (sector_summary['Raw_Score'] / max_val * 10).round(2)
    else:
        sector_summary['Strength Score'] = 0

    sector_summary = sector_summary.sort_values(by='Strength Score', ascending=False)

    # Color logic: Green for positive, Red for negative
    bar_colors = ['#00E676' if score >= 0 else '#FF1744' for score in sector_summary['Strength Score']]

    st.subheader("📊 Sector Momentum Ranking")
    
    fig_bar = go.Figure(data=[
        go.Bar(
            x=sector_summary['Sector'],
            y=sector_summary['Strength Score'],
            text=sector_summary['Strength Score'],  # Show exact value on top of bar
            textposition='outside',
            marker_color=bar_colors,
            marker_line_color=bar_colors,
            width=0.45  # Slim sleek bars
        )
    ])
    
    fig_bar.update_layout(
        template="plotly_dark",
        height=450,
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        xaxis=dict(
            tickangle=0,  # Horizontal Labels
            showgrid=False,
            title=None,
            tickfont=dict(size=11, color='#c9d1d9')
        ),
        yaxis=dict(
            title="Strength Score (-10 to +10)",
            range=[-11.5, 11.5],  # Padding for text labels
            showgrid=True,
            gridcolor="#21262d",
            zeroline=True,
            zerolinecolor="#30363d",
            zerolinewidth=1.5
        ),
        margin=dict(t=30, b=50, l=40, r=20)
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)
