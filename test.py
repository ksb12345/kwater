import gradio as gr
from functools import partial

message_list = [
    ("질문 1", "답변 1"),
    ("질문 2", "답변 2"),
    ("질문 3", "답변 3"),
    ("질문 4", "답변 4"),
    ("질문 5", "답변 5"),
]

selected_index = None  # 선택한 메시지의 인덱스를 저장하는 변수

def handle_button_click(idx):
    global selected_index
    selected_index = idx
    question, _ = message_list[idx]
    chatbot.update(f"선택한 질문: {question}")
    if use_prefix_dropdown.value == "kwater":
        chatbot.set_prefix("kwater")
    else:
        chatbot.set_perfix("일반")

def handle_user_input(user_input):
    global selected_index
    if selected_index is not None:
        _, answer_content = message_list[selected_index]
        chatbot.update(answer_content)
        selected_index = None  # 선택한 인덱스 초기화
        chatbot.set_prefix(f"{use_prefix_dropdown.value} ")

with gr.Blocks(css="#chatbot .overflow-y-auto{height:750px}") as demo:
    with gr.Row():
        gr.HTML(
            '''<div style="text-align: center; max-width: 500px; margin: 0 auto;">
                <div>
                    <h1>Kwater gpt </h1>
                </div>
                <div>
                    beomi/KoAlpaca-Polyglot-12.8, 5.8B
                </div>
            </div>'''
        )

    with gr.Row():
        chatbot = gr.Chatbot(elem_id="chatbot")

    with gr.Row():
        use_prefix_dropdown = gr.Dropdown(["kwater", "일반"], default="일반")

    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="메세지를 입력하세요...").style(
            container=False
        )

    for idx, (question, _) in enumerate(message_list):
        btn_label = question
        btn = gr.Button(btn_label, style="font-size: 14px; padding: 10px 15px; width: 100px;")  # 버튼 생성
        btn.click(partial(handle_button_click, idx))  # 버튼 클릭 이벤트 연결

    txt.submit(handle_user_input)  # 사용자 입력 제출 이벤트

demo.launch(debug=True, server_name="0.0.0.0", share=True)
