import time
import requests
import sys
import os

# Rustコア（venv内にインストール済み）をインポート
try:
    import ouroborosx_core as rust_core
    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False
    print("⚠️ Rust Core が見つかりません。")

class Orchestrator:
    def __init__(self, p2p_url):
        self.p2p_url = p2p_url
        # 100万体のエージェントを初期化
        self.count = 1_000_000
        self.agents_x = [0.0] * self.count
        self.agents_y = [0.0] * self.count
        print(f"🧠 Orchestrator initialized for {self.count} agents.")

    def step(self, tick):
        print(f"\n--- Tick {tick} ---")

        # 1. Rustで超高速演算
        if RUST_AVAILABLE:
            start = time.time()
            self.agents_x, self.agents_y = rust_core.update_agents(
                self.agents_x, self.agents_y, self.count
            )
            elapsed = time.time() - start
            print(f"⚡ Rust計算時間: {elapsed:.4f} 秒")
        
        # 2. GoのP2Pノードと同期（状態を送受信）
        try:
            # 現在の状態をPOST
            payload = {"energy": 1000.0 + (tick * 10), "tick": tick}
            requests.post(self.p2p_url + "/sync", json=payload, timeout=1)
            
            # 全ノードの合意状態をGET
            res = requests.get(self.p2p_url + "/sync", timeout=1)
            state = res.json()
            print(f"🔗 P2P同期成功: {state}")
        except Exception as e:
            print(f"⚠️ P2P通信失敗: {e}")

if __name__ == "__main__":
    p2p_url = "http://localhost:8080"
    orch = Orchestrator(p2p_url)
    
    for tick in range(1, 6):
        orch.step(tick)
        time.sleep(1)
    
    print("\n✅ ポリグロット・エンジン、全工程完了。")