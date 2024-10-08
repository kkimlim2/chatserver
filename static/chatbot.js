// 채팅 메시지를 표시할 DOM
const chatMessages = document.querySelector('#chat-messages');
// 사용자 입력 필드
const userInput = document.querySelector('#user-input input');
// 전송 버튼
const sendButton = document.querySelector('#user-input button');
// 발급받은 OpenAI API 키를 변수로 저장
const apiKey = '발급받은 API키 입력';
// OpenAI API 엔드포인트 주소를 변수로 저장
const Endpoint = '/chat'
function addMessage(sender, message) {
    // 새로운 div 생성
    const messageElement = document.createElement('div');
    // 생성된 요소에 클래스 추가
    messageElement.className = 'message';
     // 채팅 메시지 목록에 새로운 메시지 추가
    messageElement.textContent = `${sender}: ${message}`;
    chatMessages.prepend(messageElement);
}

//api 요청
async function fetchAIResponse(prompt){
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify({
            messages:[{
                role: "user",
                content: prompt
            }]
        })
    }
    try{
        const response = await fetch(Endpoint, requestOptions);
        const data = await response.json();
        const aiRespone = data['result'];
        return aiRespone;
    }
    catch (error){
        console.error('API 호출 중 오류 발생', error);
        return 'API 호출 중 오류 발생'
    }
}
// 전송 버튼 클릭 이벤트 처리
sendButton.addEventListener('click', async () => {
    // 사용자가 입력한 메시지
    const message = userInput.value.trim();
    // 메시지가 비어있으면 리턴
    if (message.length === 0) return;
    // 사용자 메시지 화면에 추가
    addMessage('나', message);
    userInput.value = '';
    // flask 에서 생성한 답변 반환 및 출력
    const response = fetch ('/', {
        method: 'POST',
        body: JSON>stringify({url: '/'}),
        headers:{
            'Content-type': 'application/json'
        }
    })

    const aiResponse = await fetchAIResponse(message);
    addMessage('혜림이: ', aiResponse);
});
// 사용자 입력 필드에서 Enter 키 이벤트를 처리
userInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        sendButton.click();
    }
});