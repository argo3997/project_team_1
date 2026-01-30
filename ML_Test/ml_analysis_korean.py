import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn.model_selection import cross_val_score, LeaveOneOut
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

# 폰트 설정 제거 (기본 영어 폰트 사용)
plt.rcParams['axes.unicode_minus'] = False
font_prop = None  # 폰트 속성 비활성화

# =============================================================================
# 1. 데이터 불러오기 및 병합
# =============================================================================

def read_csv_auto(path):
    for enc in ['utf-8', 'cp949', 'euc-kr', 'utf-8-sig']:
        try:
            return pd.read_csv(path, encoding=enc)
        except:
            continue
    return None

df_search = read_csv_auto(r'C:\Users\Administrator\Desktop\Team2_project/x축y축최종.csv') # CSV파일 경로 확인
df_hybrid = read_csv_auto(r'C:\Users\Administrator\Desktop\Team2_project/Post_핫플레이스_하이브리드_랭킹_EUC-KR.csv') # CSV파일 경로 확인

print("=" * 70)
print("1. 데이터 로드 완료")
print("=" * 70)

df_hybrid = df_hybrid.rename(columns={'행정동_코드_명': '행정동'})
df = pd.merge(df_search, df_hybrid, on='행정동', how='inner', suffixes=('_검색', '_하이브리드'))

if '하이브리드_점수_검색' in df.columns:
    df['하이브리드_점수'] = df['하이브리드_점수_검색']
    df = df.drop(columns=['하이브리드_점수_검색', '하이브리드_점수_하이브리드'])

print(f"병합 후 데이터: {len(df)}개 상권")

# =============================================================================
# 2. 라이징 상권 라벨링
# =============================================================================

df = df.sort_values('하이브리드_점수', ascending=False).reset_index(drop=True)
df['라이징여부'] = 0
df.loc[:3, '라이징여부'] = 1

print(f"\n라이징 성공 상권 (상위 4개):")
print(df[df['라이징여부'] == 1][['행정동', '하이브리드_점수']].to_string(index=False))

# =============================================================================
# 3. 특성 변수 준비
# =============================================================================

feature_cols = ['CAGR', 'avg_naver', 'blog_post', 'Model2_점수', '핫플_유사도_점수', 
                'MZ_매출_비중', '상권_유입_강도', '주말_매출_비중', '카페_밀집도']
available_features = [col for col in feature_cols if col in df.columns]

X = df[available_features]
y = df['라이징여부']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# =============================================================================
# 4. 모델 학습
# =============================================================================

print("\n" + "=" * 70)
print("2. 모델 성능 비교 (Leave-One-Out CV)")
print("=" * 70)

loo = LeaveOneOut()
models = {
    'Logistic Regression': LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000),
    'Decision Tree': DecisionTreeClassifier(max_depth=2, class_weight='balanced', random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=50, max_depth=2, class_weight='balanced', random_state=42)
}

for name, model in models.items():
    scores = cross_val_score(model, X_scaled, y, cv=loo, scoring='accuracy')
    print(f"{name}: {scores.mean():.3f}")

# =============================================================================
# 5. Feature Importance
# =============================================================================

print("\n" + "=" * 70)
print("3. Feature Importance (변수 중요도)")
print("=" * 70)

rf_model = RandomForestClassifier(n_estimators=50, max_depth=2, class_weight='balanced', random_state=42)
rf_model.fit(X_scaled, y)

importance_df = pd.DataFrame({
    '변수': available_features,
    '중요도': rf_model.feature_importances_
}).sort_values('중요도', ascending=False)

print(importance_df.to_string(index=False))

# Feature Importance 시각화
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#e74c3c' if i < 3 else '#3498db' for i in range(len(importance_df))]
bars = ax.barh(range(len(importance_df)), importance_df['중요도'], color=colors)
ax.set_yticks(range(len(importance_df)))
ax.set_yticklabels(importance_df['변수'], fontproperties=font_prop)
ax.set_xlabel('Importance Score', fontsize=12)
ax.set_title('Feature Importance for Rising District Prediction', fontsize=14, fontweight='bold')
ax.invert_yaxis()

for i, (bar, val) in enumerate(zip(bars, importance_df['중요도'])):
    ax.text(val + 0.01, i, f'{val:.3f}', va='center', fontsize=10)

plt.tight_layout()
plt.savefig('feature_importance_kr.png', dpi=150, bbox_inches='tight')
plt.close()

# =============================================================================
# 6. 라이징 확률 예측
# =============================================================================

print("\n" + "=" * 70)
print("4. 라이징 확률 예측 결과")
print("=" * 70)

lr_model = LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000)
lr_model.fit(X_scaled, y)
df['라이징_확률'] = lr_model.predict_proba(X_scaled)[:, 1]

result_df = df[['행정동', '라이징여부', '라이징_확률', 'CAGR', 'MZ_매출_비중', '하이브리드_점수']].copy()
result_df = result_df.sort_values('라이징_확률', ascending=False)

print("\n[전체 상권 라이징 확률 순위]")
print(result_df.to_string(index=False))

# 라이징 확률 시각화
fig, ax = plt.subplots(figsize=(12, 10))

colors = []
for _, row in result_df.iterrows():
    if row['라이징여부'] == 1:
        colors.append('#e74c3c')
    elif row['라이징_확률'] > 0.5:
        colors.append('#3498db')
    else:
        colors.append('#95a5a6')

bars = ax.barh(range(len(result_df)), result_df['라이징_확률'], color=colors)
ax.set_yticks(range(len(result_df)))
ax.set_yticklabels(result_df['행정동'], fontproperties=font_prop)
ax.axvline(x=0.5, color='#333', linestyle='--', linewidth=1, alpha=0.7)
ax.set_xlabel('Rising Probability', fontsize=12)
ax.set_title('Rising District Probability Ranking', fontsize=14, fontweight='bold')
ax.invert_yaxis()
ax.set_xlim(0, 1)

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#e74c3c', label='Success (Top 4)'),
    Patch(facecolor='#3498db', label='Rising Candidate'),
    Patch(facecolor='#95a5a6', label='Others')
]
ax.legend(handles=legend_elements, loc='lower right')

plt.tight_layout()
plt.savefig('rising_probability_kr.png', dpi=150, bbox_inches='tight')
plt.close()

# =============================================================================
# 7. K-Means 클러스터링
# =============================================================================

print("\n" + "=" * 70)
print("5. K-Means 클러스터링 분석")
print("=" * 70)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['클러스터'] = kmeans.fit_predict(X_scaled)

cluster_summary = df.groupby('클러스터')[available_features + ['라이징여부']].mean()
print(cluster_summary.round(3))

# 클러스터 시각화
fig, ax = plt.subplots(figsize=(10, 8))

cluster_colors = {0: '#e74c3c', 1: '#3498db', 2: '#2ecc71'}
cluster_names = {0: 'Cluster 0', 1: 'Cluster 1', 2: 'Cluster 2'}

for cluster in df['클러스터'].unique():
    cluster_data = df[df['클러스터'] == cluster]
    marker = 's' if cluster_data['라이징여부'].mean() > 0.5 else 'o'
    ax.scatter(
        cluster_data['CAGR'],
        cluster_data['MZ_매출_비중'],
        c=cluster_colors[cluster],
        s=150,
        alpha=0.7,
        label=cluster_names[cluster],
        edgecolors='white',
        linewidth=2,
        marker=marker
    )
    
    for _, row in cluster_data.iterrows():
        ax.annotate(
            row['행정동'][:4],
            (row['CAGR'], row['MZ_매출_비중']),
            fontsize=8,
            ha='center',
            va='bottom',
            fontproperties=font_prop
        )

ax.axhline(y=df['MZ_매출_비중'].median(), color='gray', linestyle='--', alpha=0.5)
ax.axvline(x=df['CAGR'].median(), color='gray', linestyle='--', alpha=0.5)

ax.set_xlabel('CAGR (Search Growth Rate)', fontsize=12)
ax.set_ylabel('MZ Sales Ratio', fontsize=12)
ax.set_title('K-Means Clustering: CAGR vs MZ Sales Ratio', fontsize=14, fontweight='bold')
ax.legend()

plt.tight_layout()
plt.savefig('cluster_analysis_kr.png', dpi=150, bbox_inches='tight')
plt.close()

print("\n" + "=" * 70)
print("완료! 한글 폰트 적용된 시각화 저장됨")
print("=" * 70)
print("- feature_importance_kr.png")
print("- rising_probability_kr.png")
print("- cluster_analysis_kr.png")
