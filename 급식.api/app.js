document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const datePicker = document.getElementById('date-picker');
    const displayDate = document.getElementById('display-date');
    const prevDayBtn = document.getElementById('prev-day');
    const nextDayBtn = document.getElementById('next-day');
    const todayBtn = document.getElementById('today-btn');
    
    const loadingState = document.getElementById('loading');
    const mealContent = document.getElementById('meal-content');
    const emptyState = document.getElementById('empty-state');
    const emptyMessage = document.getElementById('empty-message');

    // Current Date State
    let currentDate = new Date();

    // Initialize
    init();

    function init() {
        // Set date to today
        updateDateDisplay();
        fetchMealData(formatDateForAPI(currentDate));

        // Event Listeners
        datePicker.addEventListener('change', (e) => {
            currentDate = new Date(e.target.value);
            updateDateDisplay();
            fetchMealData(formatDateForAPI(currentDate));
        });

        prevDayBtn.addEventListener('click', () => {
            currentDate.setDate(currentDate.getDate() - 1);
            updateDateDisplay();
            fetchMealData(formatDateForAPI(currentDate));
        });

        nextDayBtn.addEventListener('click', () => {
            currentDate.setDate(currentDate.getDate() + 1);
            updateDateDisplay();
            fetchMealData(formatDateForAPI(currentDate));
        });

        todayBtn.addEventListener('click', () => {
            currentDate = new Date();
            updateDateDisplay();
            fetchMealData(formatDateForAPI(currentDate));
        });
    }

    function updateDateDisplay() {
        const year = currentDate.getFullYear();
        const month = String(currentDate.getMonth() + 1).padStart(2, '0');
        const day = String(currentDate.getDate()).padStart(2, '0');
        
        // Update input value
        datePicker.value = `${year}-${month}-${day}`;
        
        // Update display text (e.g., 2024. 05. 15 (수))
        const days = ['일', '월', '화', '수', '목', '금', '토'];
        const dayOfWeek = days[currentDate.getDay()];
        displayDate.textContent = `${year}. ${month}. ${day} (${dayOfWeek})`;
    }

    function formatDateForAPI(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}${month}${day}`;
    }

    async function fetchMealData(dateString) {
        showLoading();

        const url = 'https://open.neis.go.kr/hub/mealServiceDietInfo';
        const params = new URLSearchParams({
            Type: 'json',
            ATPT_OFCDC_SC_CODE: 'B10', // 서울특별시교육청
            SD_SCHUL_CODE: '7010703',  // 자운고등학교
            MLSV_YMD: dateString
        });

        try {
            const response = await fetch(`${url}?${params.toString()}`);
            const data = await response.json();

            if (data.mealServiceDietInfo) {
                const rows = data.mealServiceDietInfo[1].row;
                renderMeals(rows);
            } else if (data.RESULT && data.RESULT.CODE === 'INFO-200') {
                showEmptyState('해당 날짜의 급식 정보가 없습니다.');
            } else {
                showEmptyState('급식 정보를 불러오는 중 오류가 발생했습니다.');
                console.error('API Error:', data);
            }
        } catch (error) {
            showEmptyState('인터넷 연결을 확인해주세요.');
            console.error('Fetch Error:', error);
        }
    }

    function renderMeals(meals) {
        mealContent.innerHTML = '';
        
        meals.forEach((meal) => {
            const mealType = meal.MMEAL_SC_NM; // 조식, 중식, 석식
            const rawMenu = meal.DDISH_NM;
            
            // 정규표현식을 사용하여 메뉴 정제 (알레르기 숫자, 불필요한 특수문자 제거)
            let cleanedMenuStr = rawMenu
                .replace(/[0-9.*]+<br\/>/g, '\n') // 숫자.*<br/> 패턴
                .replace(/<br\/>/g, '\n')         // 남은 <br/>
                .replace(/[^가-힣a-zA-Z\s\n]/g, ''); // 한글, 영문, 공백, 줄바꿈 제외 모두 제거
            
            // 빈 줄 제거 및 배열로 변환
            const menuItems = cleanedMenuStr
                .split('\n')
                .map(item => item.trim())
                .filter(item => item.length > 0);

            // 카드 생성
            const card = document.createElement('article');
            card.className = 'meal-card';
            
            const typeBadge = document.createElement('div');
            typeBadge.className = `meal-type ${mealType}`;
            typeBadge.textContent = mealType;
            
            const menuList = document.createElement('ul');
            menuList.className = 'menu-list';
            
            menuItems.forEach(item => {
                const li = document.createElement('li');
                li.className = 'menu-item';
                li.textContent = item;
                menuList.appendChild(li);
            });
            
            card.appendChild(typeBadge);
            card.appendChild(menuList);
            mealContent.appendChild(card);
        });

        showContent();
    }

    function showLoading() {
        loadingState.classList.remove('hidden');
        mealContent.classList.add('hidden');
        emptyState.classList.add('hidden');
    }

    function showContent() {
        loadingState.classList.add('hidden');
        mealContent.classList.remove('hidden');
        emptyState.classList.add('hidden');
    }

    function showEmptyState(message) {
        loadingState.classList.add('hidden');
        mealContent.classList.add('hidden');
        emptyState.classList.remove('hidden');
        emptyMessage.textContent = message;
    }
});
