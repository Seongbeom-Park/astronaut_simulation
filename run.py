#!/bin/python3
'''우주비행사 선발과정 시뮬레이션 스크립트

총점수가 높은 지원자부터 우주비행사로 선발됩니다.
기술점수와 운점수, 기술점수 가중치, 운점수 가중치로 총점수가 정해집니다.
기술점수는 시뮬레이션 실행 시 처음에만 초기화되며, 운점수는 매 시뮬레이션마다 초기화됩니다.

선발된 우주비행사의 평균 기술점수와 평균 운점수를 출력합니다
또한, 높은 기술점수를 갖는 지원자들 중 평균적으로 몇 명이 우주비행사로 선발되었는지 출력합니다.
'''
import argparse
import numpy as np
import pandas as pd

def create_candidate(count):
    '''지원자들의 기술점수를 초기화합니다.'''
    return pd.DataFrame(np.random.rand(count) * 100, columns=['skill'])

def update_luck(candidate):
    '''지원자들의 운점수를 초기화합니다.'''
    count = len(candidate)
    candidate['luck'] = np.random.rand(count) * 100

def select_top_candidate_ids(candidate, count, ratio_skill, ratio_luck):
    '''총점수가 높은 지원자들의 아이디를 반환합니다.'''
    score = ratio_skill * candidate['skill']
    if ratio_luck != 0:
        score += ratio_luck * candidate['luck']
    selected = score.sort_values().tail(count)
    return selected.index

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='우주비행사 선별과정 시뮬레이션')
    parser.add_argument('count_candidate', type=int, help='지원자 수')
    parser.add_argument('count_astronaut', type=int, help='선발될 우주비행사 수')
    parser.add_argument('count_simulation', type=int, help='시뮬레이션 반복 횟수')
    parser.add_argument('ratio_skill', type=float, help='기술 점수 비중')
    parser.add_argument('ratio_luck', type=float, help='운 점수 비중')
    parser.add_argument('--seed', type=int, help='랜덤 시드 설정')

    args = parser.parse_args()
    print('=== 실험 설정 ===')
    print('지원자 수:', args.count_candidate)
    print('선발될 우주비행사 수:', args.count_astronaut)
    print('시뮬레이션 횟수:', args.count_simulation)
    print('운이 주는 영향:', args.ratio_luck / (args.ratio_skill + args.ratio_luck) * 100, '%')
    print('랜덤 시드:', args.seed)
    print()

    np.random.seed(args.seed)

    skill_sum = 0.0
    luck_sum = 0.0
    top_sum = 0

    all_candidate = create_candidate(args.count_candidate)
    skilled_candidate_ids = select_top_candidate_ids(all_candidate, args.count_astronaut, 100, 0)
    for expr in range(args.count_simulation):
        update_luck(all_candidate)
        selected_candidate_ids = select_top_candidate_ids(all_candidate, args.count_astronaut,
                                                          args.ratio_skill, args.ratio_luck)
        top_candidate = all_candidate.filter(items=selected_candidate_ids, axis=0)

        skill_sum += sum(top_candidate['skill'])
        luck_sum += sum(top_candidate['luck'])
        top_sum += len(selected_candidate_ids.intersection(skilled_candidate_ids))

    print('=== 실험 결과 ===')
    skill_mean = skill_sum / args.count_simulation / args.count_astronaut
    luck_mean = luck_sum / args.count_simulation / args.count_astronaut
    print('발탁된 우주비행사의 평균 기술 점수:', skill_mean)
    print('발탁된 우주비행사의 평균 운 점수:', luck_mean)

    top_mean = top_sum / args.count_simulation
    print('지원자 상위 11명이 우주비행사로 발탁되는 평균 인원:', top_mean)
