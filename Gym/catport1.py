import gym
env = gym.make('CartPole-v1', render_mode="rgb_array")  # 예로 'CartPole-v1' 환경을 사용
env.reset()  # 환경을 초기화

for _ in range(1000):
    frame = env.render()  # 환경을 시각화
    action = env.action_space.sample()  # 임의의 행동 선택
    observation, reward, terminated, truncated, info = env.step(action)  # 선택한 행동 실행

    if terminated or truncated:
        env.reset()

env.close()  # 환경 닫기
