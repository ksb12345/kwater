<<<<<<< HEAD
torchrun --nproc_per_node=4 --master_port=34321 train.py \
    --model_name_or_path /workspace/llama/llama-7b \
    --data_path ./alpaca_data.json \
    --bf16 True \
    --output_dir ./KoAlpaca \
    --num_train_epochs 3 \
    --per_device_train_batch_size 4 \
    --per_device_eval_batch_size 4 \
    --gradient_accumulation_steps 8 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 2000 \
    --save_total_limit 1 \
    --learning_rate 2e-5 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --fsdp "full_shard auto_wrap" \
    --fsdp_transformer_layer_cls_to_wrap 'LlamaDecoderLayer' \
    --tf32 True
=======
# Works on A100 80G x4
torchrun --nproc_per_node=4 --master_port=34321 run_clm.py \
--model_name_or_path='EleutherAI/polyglot-ko-12.8b' \
--train_file='KoAlpaca_v1.1a_textonly.json' \
--num_train_epochs=2 \
--block_size=1024 \
--per_device_train_batch_size=1 \
--gradient_accumulation_steps=64 \
--torch_dtype=float16 \
--fp16 \
--output_dir='polyglot-12.8b-koalpaca-v1.1b' \
--deepspeed=ds_zero3-nooffload.json \
--do_train \
--save_strategy='epoch' \
--logging_strategy='steps' \
--logging_first_step \
--save_total_limit=1 \
--run_name='polyglot-12.8b-koalpaca-v1.1b-ga64'
>>>>>>> 3aee68d84ea22a31c11598d1082362713568ae17
