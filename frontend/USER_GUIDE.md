| 단계 | 위치(CSS) | 설명 | 파일 |
| --- | --- | --- | --- |
| 1 | `select.tie-select` | 경기일(TIE 날짜) 드롭다운입니다. 날짜를 선택하면 아래 목록이 필터링됩니다. | `CoderList.vue` |
| 1 | `select.form-control` | [
            'Match 번호를 선택합니다.',
            '선택 시 해당 Match 의 5게임 목록이 자동 로드됩니다.'
            ].join('\n') | `CoderOfficials.vue` |
| 1 | `div.scoreboard` | [
           '현재 Match 번호와 선택된 타이머 종류(Time Target)가 표시됩니다.',
           '팀명과 현재 SCORE 를 실시간으로 확인할 수 있습니다.'
           ].join('\n') | `CoderPage.vue` |
| 1 | `div.form-group.left` | 대회를 선택하면 해당 대회의 팀·선수 목록이 로드됩니다. | `CoderTie.vue` |
| 1 | `input` | [
              '로그인에 사용할 사용자 ID(이메일)를 입력합니다.'
              ].join('\\n') | `Login.vue` |
| 1 | `button.btn.coder` | [
                '경기 진행용 Coder 화면으로 이동합니다.',
                'Match·Timer·Score를 실시간 제어합니다.'
              ].join('\n') | `MainPage.vue` |
| 1 | `div.top-bar` | [
                'Add Muitiple Officials : 한 화면에서 여러 심판을 동시에 등록합니다. + Add Row 로 행을 추가한 뒤 Save 를 누르세요.',
                'Delete Selected : 하단 체크 박스에 선택된 심판을 삭제합니다. '
       ].join('\n') | `OfficialList.vue` |
| 1 | `select.tour-select` | [
                '특정 대회(Tournament)만 선택해 팀 목록을 필터링합니다.',
                '전체 보려면 빈 값(맨 위 옵션)으로 돌려놓으세요.'
                ].join('\n') | `TeamList.vue` |
| 1 | `select.form-control` | [
                    '팀

이 소속될 대회를 선택하세요. 선택 후 선수·팀 정보가 해당 대회에 저장됩니다.'
                    ].join('\n') | `TeamPage.vue` |
| 1 | `section.tour-list` | [
                 '대회 카드를 클릭하면 상세·편집 페이지로 이동합니다.',
                 '표시: 국가·도시·기간 – 대회명'].join('\n') | `TourList.vue` |
| 1 | `label` | [
                 '대회 전체 이름을 입력하세요.',
                 '예: 2025 Korea Open BXL Badminton'
                 ].join('\n') | `TourPage.vue` |
| 2 | `article.tie-card` | `${tie.tie_no} TIE 카드: 상세·진행 페이지로 이동하려면 클릭하세요.` | `CoderList.vue` |
| 2 | `select.form-control` | [
            '심판을 배정할 개별 Game 을 선택합니다.',
            '아래 체크박스를 선택하면 비활성화되고 5게임에 동일 배정이 적용됩니다.',
            '✔ 체크하면 Match 내 5게임 모두에 동일한 심판 배정이 적용됩니다.',
            '해제 시에는 개별 Game 을 선택해 따로 배정할 수 있습니다.'
            ].join('\n') | `CoderOfficials.vue` |
| 2 | `div.label-row` | [
             '하단 Clock Setting에서 수정할 시간을 선택 가능합니다.',
             '노란색으로 강조된 박스가 현재 조정 대상(clock target)입니다.',
             ].join('\n') | `CoderPage.vue` |
| 2 | `input.form-control` | 경기일을 지정합니다. | `CoderTie.vue` |
| 2 | `input` | [
              '비밀번호를 입력합니다.',
              'Caps Lock 상태에 주의하세요.'
              ].join('\\n') | `Login.vue` |
| 2 | `button.btn.scorer` | [
                '실시간 입력기 화면으로 이동합니다.',
                ].join('\n') | `MainPage.vue` |
| 2 | `th` | [
                      '해당 심판 정보를 팝업으로 수정합니다.',
                      '변경 후 Save 를 누르면 즉시 DB 에 반영됩니다.'
                      ].join('\n') | `OfficialList.vue` |
| 2 | `section.team-list` | [
                 '팀(Team) 카드를 눌러 상세·편집 화면으로 이동합니다.',
                 '표시: [대회·도시] 팀명 (선수 수)'
                 ].join('\n') | `TeamList.vue` |
| 2 | `input.form-control` | ['팀명을 입력합니다. 예: Seoul Shuttlers'].join('\n') | `TeamPage.vue` |
| 2 | `button.btn.btn-primary` | [
                 '새 대회(Tournament)를 등록합니다.',
                 '이전 화면으로 돌아갑니다.',
                 '홈 대시보드로 이동합니다.'
                 ].join('\n') | `TourList.vue` |
| 2 | `label` | [
                 '대회 시작 / 종료 날짜를 선택합니다.'
                 ].join('\n') | `TourPage.vue` |
| 3 | `button.btn-clear` | [
                  '현재 화면에 보이는 모든 심판 배정 정보를 초기화합니다.'
                  ].join('\n') | `CoderOfficials.vue` |
| 3 | `div.reset-box` | [
               '양 팀의 SCORE를 0 으로 초기화합니다.',
               'Non‑Stop Mode가 체크되어 있으면 Warn Up에서 Mach Clock으로 지동으로 넘어 갑니다.',
               '체크되어 있지 않으면 운영자가 Match Clock 상태에서 다시 START를 클릭해야 합니다.'
             ].join('\n') | `CoderPage.vue` |
| 3 | `select.form-control` | Tie 번호(1~9) 를 지정합니다. | `CoderTie.vue` |
| 3 | `button.login-btn` | [
                  '입력한 ID / Password 로 로그인합니다.',
                  '오류 시 알림 메시지가 표시됩니다.'
                  ].join('\\n') | `Login.vue` |
| 3 | `button.btn.tour` | [
                '대회(Tournament) 정보를 조회·편집합니다.'
                ].join('\n') | `MainPage.vue` |
| 3 | `div.modal-content` | [
       '선택한 심판의 이름·국적·성별을 수정합니다.',
       'Save 로 반영, Cancel 로 취소합니다.'
     ].join('\n') | `OfficialList.vue` |
| 3 | `footer.team-footer` | [
                '새로등록 : 새 팀을 등록합니다.대회·도시·팀명·선수를 입력하는 페이지로 이동합니다.',
                '뒤로가기 : 이전 화면(대회 리스트 등)으로 돌아갑니다.',
                '메인가기 : 홈 대시보드로 이동합니다.'
                ].join('\n') | `TeamList.vue` |
| 3 | `div.player-wrapper` | ['이미 등록된 선수 정보를 수정하려면 각 필드를 직접 편집하세요.',
                  '빨간 버튼으로 해당 선수를 삭제할 수 있습니다.'].join('\n') | `TeamPage.vue` |
| 3 | `label` | [
                 '대회 개최 국가와 도시를 선택 그리고 하단에 체육관을 구체적으로 입력 '
                 ].join('\n') | `TourPage.vue` |
| 4 | `div.warmup-clock-setting-row` | [
                 '화살표(↑↓)로 SCORE 를 증감합니다.',
                 '각 칸(POINT, GAME) 도 동일한 방식으로 조정합니다.',
                 '팀 B 역시 동일하게 조정 가능합니다.'
               ].join('\n') | `CoderPage.vue` |
| 4 | `select.form-control` | [
                '팀1을 선택합니다.',
                '이미 선택된 팀2와 동일 팀은',
                '비활성화됩니다.'
              ].join('\n') | `CoderTie.vue` |
| 4 | `button.btn.team` | [
                '팀·선수·경기(Game) 데이터를 관리합니다.'
                ].join('\\n') | `MainPage.vue` |
| 4 | `div.player-row-line` | ['여기에 새 선수 정보를 입력합니다.', '모든 필수 항목을 채우고 “등록” 버튼(5번)을 누르세요.'].join('\n') | `TeamPage.vue` |
| 4 | `div.button-container` | [
             '저장 : 모든 정보를 서버(DB)에 저장합니다',
             '종료 : 작업을 취소하고 메인 화면으로 돌아갑니다.',
             '삭제 : 현재 대회를 완전히 삭제합니다'
             ].join('\n') | `TourPage.vue` |
| 5 | `table.official-table` | [
        '역할별 Assign 버튼을 눌러 심판을 지정합니다.',
        '이미 배정된 심판은 리스트에서 회색으로 표시되어 선택할 수 없습니다.'
        ].join('\n') | `CoderOfficials.vue` |
| 5 | `div.extra-label-row` | [
               'Game 버튼(Gm 1~4)을 눌러 현재 경기 게임 번호를 설정합니다.',
               'SD 는 Sudden Death, SS 는 Shuttle Showdown 상태 표시입니다.'
               ].join('\n') | `CoderPage.vue` |
| 5 | `select.form-control` | [
              '팀2를 선택합니다.',
              'Team1과 중복되지 않도록 주의하세요.'
            ].join('\n') | `CoderTie.vue` |
| 5 | `div.matches-container` | [ '각 Match 행에서 매치 타입을 고르면 자동으로 필요한 선수 수(점수)가 설정됩니다.'
           , '수정 시에는 출전하는 선수만 교체가 가능합니다.'].join('\n') | `CoderTie.vue` |
| 5 | `button.btn.official` | [
                '심판(Official) 배정·조회 화면으로 이동합니다.'
                ].join('\\n') | `MainPage.vue` |
| 5 | `button.btn.btn-register` | [
             '등록 : 새 선수 입력 행의 내용을 목록에 추가합니다.',
             '저장 : 모든 변경 사항을 서버(DB)에 저장합니다.',
             '종료 : 작업을 종료하고 메인 화면으로 돌아갑니다.'
             ].join('\n') | `TeamPage.vue` |
| 6 | `div.warmup-clock-setting-box` | [
                 'Clock Setting : 클릭하면 WARMUP/MATCH/BREAK 중 하나가 선택됩니다.',
                 'START/PAUSE/RESET : 시간을 시작/중지/초기화 하는 버튼입니다.'
               ].join('\n') | `CoderPage.vue` |
| 7 | `div.warmup-control-box.extra-label-control` | [
                 'Next Match : 모든 데이터가 저장되고 다음 Match 로 이동합니다.',
                 'Result : 현재 Match 결과를 서버에 전송합니다.'
                 ].join('\n') | `CoderPage.vue` |
| 99 | `footer.tie-footer` | [
                '새로등록: 신규 TIE(빈 경기) 생성 화면으로 이동합니다.',
                '뒤로가기: 이전 화면으로 돌아갑니다.',
                '메인가기: 메인 대시보드로 이동합니다.'
              ].join('\n') | `CoderList.vue` |
| 99 | `button.save-btn` | [ '저장:현재 입력 내용을 저장합니다.', '종료:저장하지 않고 대시보드로 돌아갑니다.'].join('\n') | `CoderOfficials.vue` |
| 99 | `button.btn.btn-save` | [ '저장:현재 입력 내용을 저장합니다.', '종료:저장하지 않고 대시보드로 돌아갑니다.'].join('\n') | `CoderTie.vue` |