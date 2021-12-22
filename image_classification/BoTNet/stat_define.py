import os
import glob
import paddle
from config import get_config
from botnet import build_botnet50 as build_model

def count_gelu(layer, input, output):
    activation_flops = 8
    x = input[0]
    num = x.numel()
    layer.total_ops += num * activation_flops 


def count_softmax(layer, input, output):
    softmax_flops = 5 # max/substract, exp, sum, divide
    x = input[0]
    num = x.numel()
    layer.total_ops += num * softmax_flops 


def count_layernorm(layer, input, output):
    layer_norm_flops = 5 # get mean (sum), get variance (square and sum), scale(multiply)
    x = input[0]
    num = x.numel()
    layer.total_ops += num * layer_norm_flops 


#cfg = './configs/xcit_nano_12_p8_224.yaml'
#input_size = (1, 3, 224, 224)
#cfg = './configs/xcit_large_24_p16_384.yaml'
#input_size = (1, 3, 384, 384)
#config = get_config(cfg)
#model = build_model(config)

#custom_ops = {paddle.nn.GELU: count_gelu,
#              paddle.nn.LayerNorm: count_layernorm,
#              paddle.nn.Softmax: count_softmax,
#            }
#print(os.path.basename(cfg))
#paddle.flops(model,
#             input_size=input_size,
#             custom_ops=custom_ops,
#             print_detail=False)


for cfg in glob.glob('./configs/*.yaml'):
    input_size = (1, 3, 224, 224)
    config = get_config(cfg)
    model = build_model(config)
    
    
    custom_ops = {paddle.nn.GELU: count_gelu,
                  paddle.nn.LayerNorm: count_layernorm,
                  paddle.nn.Softmax: count_softmax,
                }
    print(os.path.basename(cfg))
    paddle.flops(model,
                 input_size=input_size,
                 custom_ops=custom_ops,
                 print_detail=False)
    print('-----------')