import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

group_A_text = {
    "exploration_interest":   np.array([52, 58, 55, 60, 53, 57, 59, 54, 56, 61, 58, 55, 57, 54, 56, 59]),  
    "knowledge_instant":      np.array([60, 64, 59, 65, 61, 63, 60, 62, 64, 61, 63, 60, 62, 65, 61, 59]),  
    "knowledge_24h":          np.array([45, 50, 47, 52, 46, 49, 51, 48, 47, 50, 49, 46, 48, 51, 47, 45]),  
    "cultural_identity":      np.array([60, 65, 62, 64, 61, 63, 65, 62, 64, 61, 63, 60, 62, 65, 61, 63])   
}

group_B_3d = {
    "exploration_interest":   np.array([70, 74, 72, 75, 71, 73, 76, 72, 74, 71, 73, 70, 72, 75, 71, 73]),  
    "knowledge_instant":      np.array([72, 76, 74, 77, 73, 75, 76, 73, 75, 72, 74, 71, 73, 76, 72, 74]),  
    "knowledge_24h":          np.array([70, 74, 72, 75, 71, 73, 75, 72, 74, 71, 73, 70, 72, 75, 71, 73]),  
    "cultural_identity":      np.array([72, 76, 74, 77, 73, 75, 76, 73, 75, 72, 74, 71, 73, 76, 72, 74])   
}

group_C_3d_dh = {
    "exploration_interest":   np.array([88, 92, 90, 93, 89, 91, 92, 89, 91, 88, 90, 87, 89, 92, 89, 91]),  
    "knowledge_instant":      np.array([83, 87, 85, 88, 84, 86, 87, 84, 86, 83, 85, 82, 84, 87, 84, 86]),  
    "knowledge_24h":          np.array([74, 78, 76, 79, 75, 77, 78, 75, 77, 74, 76, 73, 75, 78, 75, 77]),  
    "cultural_identity":      np.array([84, 88, 86, 89, 85, 87, 88, 85, 87, 84, 86, 83, 85, 88, 85, 87])   
}

dimensions = ["exploration_interest", "knowledge_instant", "knowledge_24h", "cultural_identity"]
dim_names = ["Exploration Interest", "Instant Knowledge Retention", "24h Knowledge Retention", "Cultural Identity"]

print("=== 三组实验描述性统计 ===")
for dim, name in zip(dimensions, dim_names):
    print(f"\n--- {name} ---")
    print(f"A组 图文: 均值={np.mean(group_A_text[dim]):.1f}%")
    print(f"B组 纯3D: 均值={np.mean(group_B_3d[dim]):.1f}%")
    print(f"C组 3D+数字人: 均值={np.mean(group_C_3d_dh[dim]):.1f}%")

print("\n\n=== 组间差异显著性检验 (独立样本t检验) ===")
for dim, name in zip(dimensions, dim_names):
    print(f"\n--- {name} ---")
    
    # A vs B
    t1, p1 = stats.ttest_ind(group_A_text[dim], group_B_3d[dim], equal_var=False)
    print(f"图文 vs 纯3D: t={t1:.3f}, p={p1:.4f} | 显著: {p1 < 0.05}")
    
    # B vs C
    t2, p2 = stats.ttest_ind(group_B_3d[dim], group_C_3d_dh[dim], equal_var=False)
    print(f"纯3D vs 3D+数字人: t={t2:.3f}, p={p2:.4f} | 显著: {p2 < 0.05}")
    
    # A vs C
    t3, p3 = stats.ttest_ind(group_A_text[dim], group_C_3d_dh[dim], equal_var=False)
    print(f"图文 vs 3D+数字人: t={t3:.3f}, p={p3:.4f} | 显著: {p3 < 0.05}")

x = np.arange(len(dim_names))
width = 0.25

means_A = [np.mean(group_A_text[d]) for d in dimensions]
means_B = [np.mean(group_B_3d[d]) for d in dimensions]
means_C = [np.mean(group_C_3d_dh[d]) for d in dimensions]

plt.figure(figsize=(10, 6))
plt.bar(x - width, means_A, width, label='Text & Image (Control)', color='#c4c4c4')
plt.bar(x, means_B, width, label='Pure 3D Scene', color='#a8d8ea')
plt.bar(x + width, means_C, width, label='3D + AI Digital Human', color='#aa96da')

plt.xticks(x, dim_names, rotation=10)
plt.ylabel('Score (%)')
plt.ylim(0, 100)
plt.title('Comparison of ICH Dissemination Effect Across Three Groups')
plt.legend()
plt.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig("experiment_result.png", dpi=300, bbox_inches='tight')
print("\n结果统计图已保存为 experiment_result.png")
