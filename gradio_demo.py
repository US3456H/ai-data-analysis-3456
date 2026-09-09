# gradio_demo.py

import os
import gradio as gr
import numpy as np

MODEL_PATH = 'workspace/linear_model.joblib'

try:
    import joblib
    model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None
except Exception:
    model = None

def predict(values):
    # values: comma separated lag values
    try:
        arr = [float(x.strip()) for x in values.split(',')]
        X = np.array(arr).reshape(1, -1)
        if model is None:
            return 'No trained sklearn model found. Please run workspace/train_and_log.py first.'
        pred = model.predict(X)[0]
        return f'预测下一个值: {pred:.4f}'
    except Exception as e:
        return f'错误: {e}'

iface = gr.Interface(fn=predict, inputs=gr.Textbox(value='1.0,2.0,3.0,4.0,5.0,6.0,7.0', label='7个滞后值, 用逗号分隔'), outputs='text', title='简单时间序列预测演示')

if __name__ == '__main__':
    iface.launch(server_name='0.0.0.0', server_port=7860, share=False)
