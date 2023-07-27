import gradio as gr
import torch
from transformers import pipeline, AutoModelForCausalLM

MODEL = "beomi/KoAlpaca-Polyglot-12.8B"
model = AutoModelForCausalLM.from_pretrained(
    MODEL,
    device_map="auto",
    load_in_8bit=True,
    revision="8bit",
    # max_memory=f'{int(torch.cuda.mem_get_info()[0]/1024**3)-2}GB'
)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=MODEL,
    # device=2,
)

def summarize(text, max_length=250):
    # Load the summarization pipeline
    summarizer = pipeline("summarization")

    # Summarize the input text
    summary = summarizer(text, max_length=max_length, min_length=50, do_sample=False)

    # Extract the summarized text from the output dictionary
    summarized_text = summary[0]['summary_text']

    return summarized_text

def answer(state, state_chatbot, text, include_prefix, do_summarize):

    if include_prefix:
        text = f"(kwater) {text}"
    else:
        text = text

    if do_summarize:
        text = summarize(text, max_length=500)   

    messages = state + [{"role": "질문", "content": text}]

    conversation_history = "\n".join(
        [f"### {msg['role']}:\n{msg['content']}" for msg in messages]
    )

    ans = pipe(
        conversation_history + "\n\n### 답변:",
        do_sample=True,
        max_new_tokens=512,
        temperature=0.9,
        top_p=0.9,
        return_full_text=False,
        eos_token_id=2,
    )

    msg = ans[0]["generated_text"]

    if "###" in msg:
        msg = msg.split("###")[0]

    new_state = [{"role": "이전 질문", "content": text}, {"role": "이전 답변", "content": msg}]

    state = state + new_state
    state_chatbot = state_chatbot + [(text, msg)]

    return state, state_chatbot, state_chatbot

state = [
    {
        "role": "맥락",
        "content": "KoAlpaca(코알파카)는 EleutherAI에서 개발한 Polyglot-ko 라는 한국어 모델을 기반으로, 자연어 처리 연구자 Beomi가 개발한 모델입니다.",
    },
    {
        "role": "맥락",
        "content": "ChatKoAlpaca(챗코알파카)는 KoAlpaca를 채팅형으로 만든 것입니다.",
    },
    {"role": "명령어", "content": "친절한 AI 챗봇인 ChatKoAlpaca 로서 답변을 합니다."},
    {
        "role": "명령어",
        "content": "인사에는 짧고 간단한 친절한 인사로 답하고, 아래 대화에 간단하고 짧게 답해주세요.",
    },
]

state_chatbot = []

def toggle_prefix(btn_value):
    global include_prefix
    include_prefix = btn_value

def toggle_summarize(btn_value):
    global do_summarize
    do_summarize = btn_value

include_prefix = True  # 초기에는 (kwater)가 포함된 형태로 시작
button = gr.ButtonGroup(["(kwater) On", "(kwater) Off"], label="Include (kwater):", default=0)
button.onclick(toggle_prefix)

checkbox = gr.Toggle(False, label="Include Summarize:")
checkbox.onclick(lambda _: toggle_summarize(checkbox))

textbox = gr.Textbox(show_label=False, placeholder="Send a message...").style(
    container=False
)

demo = gr.Interface(
    fn=answer,
    inputs=[
        button,
        checkbox,
        gr.Param("State", gr.JSON, state),
        gr.Param("State Chatbot", gr.JSON, state_chatbot),
        textbox,
    ],
    outputs="json",
    examples=[
        ["Include (kwater):", "Include Summarize:", "State", "State Chatbot", "Send a message..."],
    ],
)

demo.launch(debug=True, server_name="0.0.0.0")
