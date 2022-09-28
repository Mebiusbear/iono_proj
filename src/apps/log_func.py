import logging

# 日志部分
# class Make_log:
#     def __init__(self,npixel,steps,pscale):
    
#         # 第一步，创建一个logger
#         logger = logging.getLogger()
#         logger.setLevel(logging.INFO)  # Log等级总开关  此时是INFO

#         # 第二步，创建一个handler，用于写入日志文件
#         logfile = 'log_file/pixel_%d_step_%d_scale_%d.log'%(npixel,steps,pscale)
#         fh = logging.FileHandler(logfile, mode='w')  # open的打开模式这里可以进行参考
#         fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关

#         # 第三步，再创建一个handler，用于输出到控制台
#         ch = logging.StreamHandler()
#         ch.setLevel(logging.WARNING)   # 输出到console的log等级的开关

#         # 第四步，定义handler的输出格式（时间，文件，行数，错误级别，错误提示）
#         formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
#         fh.setFormatter(formatter)
#         ch.setFormatter(formatter)

#         # 第五步，将logger添加到handler里面
#         logger.addHandler(fh)
#         logger.addHandler(ch)
    
#     def write_info(self,message):
#         logging.info(message)




def init_logging(npixel,steps,pscale):
    logging.basicConfig(
        filename='log_file/pixel_%d_step_%d_scale_%d.log'%(npixel,steps,pscale),
        filemode="w",
        format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s",
        datefmt="%d/%m/%Y %I:%M:%S %p",
        level=logging.INFO,
    )
    logging.info("This is Liuyihong Project!\n")

def printf_args(args):
    for arg in args.__dict__:
        mes = "%s : %s"%(arg,args.__dict__[arg])
        if arg == "scheduler":
            mes += "\n"
        logging.info(mes)
