# ethical_market.py
class EthicalMarket:
    def __init__(self, total_energy):
        self.total_energy = total_energy
        self.contributors = []

    def add_contributor(self, name, contribution_score):
        self.contributors.append({"name": name, "score": contribution_score, "reward": 0.0})

    def distribute_rewards(self):
        # 貢献度の2乗に比例させることで、高い倫理（多大な貢献）を強く優遇する
        total_score_squared = sum(c["score"] ** 2 for c in self.contributors)
        if total_score_squared == 0:
            return

        for c in self.contributors:
            c["reward"] = (c["score"] ** 2 / total_score_squared) * self.total_energy

    def report(self):
        print("=== 倫理的報酬分配レポート ===")
        for c in self.contributors:
            print(f"{c['name']}: 貢献度={c['score']:.2f}, 獲得報酬={c['reward']:.2f} ATH")

if __name__ == "__main__":
    market = EthicalMarket(total_energy=100)
    market.add_contributor("Node_A (誠実)", 0.9)
    market.add_contributor("Node_B (普通)", 0.5)
    market.add_contributor("Node_C (怠惰)", 0.1)
    
    market.distribute_rewards()
    market.report()