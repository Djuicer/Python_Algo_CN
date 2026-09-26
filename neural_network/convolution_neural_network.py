"""
 - - - - - -- - - - - - - - - - - - - - - - - - - - - - -
名称 - - CNN - 用于图像识别的卷积神经网络
目标 - - 识别手写文字图像
详情：共包含 5 层神经网络
        * 卷积层
        * 池化层
        * BP 输入层
        * BP 隐藏层
        * BP 输出层
Author: Stephen Lee
Github: 245885195@qq.com
Date: 2017.9.20
- - - - - -- - - - - - - - - - - - - - - - - - - - - - -
"""

import pickle

import numpy as np
from matplotlib import pyplot as plt


class CNN:
    def __init__(
        self, conv1_get, size_p1, bp_num1, bp_num2, bp_num3, rate_w=0.2, rate_t=0.2
    ) -> None:
        """
        :param conv1_get: [a,c,d]，卷积核的大小、数量和步长
        :param size_p1: 池化大小
        :param bp_num1: 展平层的单元数
        :param bp_num2: 隐藏层的单元数
        :param bp_num3: 输出层的单元数
        :param rate_w: 权重学习率
        :param rate_t: 阈值学习率
        """
        self.num_bp1 = bp_num1
        self.num_bp2 = bp_num2
        self.num_bp3 = bp_num3
        self.conv1 = conv1_get[:2]
        self.step_conv1 = conv1_get[2]
        self.size_pooling1 = size_p1
        self.rate_weight = rate_w
        self.rate_thre = rate_t
        rng = np.random.default_rng()
        self.w_conv1 = [
            np.asmatrix(-1 * rng.random((self.conv1[0], self.conv1[0])) + 0.5)
            for i in range(self.conv1[1])
        ]
        self.wkj = np.asmatrix(-1 * rng.random((self.num_bp3, self.num_bp2)) + 0.5)
        self.vji = np.asmatrix(-1 * rng.random((self.num_bp2, self.num_bp1)) + 0.5)
        self.thre_conv1 = -2 * rng.random(self.conv1[1]) + 1
        self.thre_bp2 = -2 * rng.random(self.num_bp2) + 1
        self.thre_bp3 = -2 * rng.random(self.num_bp3) + 1

    def save_model(self, save_path) -> None:
        # 使用 pickle 保存模型字典
        model_dic = {
            "num_bp1": self.num_bp1,
            "num_bp2": self.num_bp2,
            "num_bp3": self.num_bp3,
            "conv1": self.conv1,
            "step_conv1": self.step_conv1,
            "size_pooling1": self.size_pooling1,
            "rate_weight": self.rate_weight,
            "rate_thre": self.rate_thre,
            "w_conv1": self.w_conv1,
            "wkj": self.wkj,
            "vji": self.vji,
            "thre_conv1": self.thre_conv1,
            "thre_bp2": self.thre_bp2,
            "thre_bp3": self.thre_bp3,
        }
        with open(save_path, "wb") as f:
            pickle.dump(model_dic, f)

        print(f"Model saved: {save_path}")

    @classmethod
    def read_model(cls, model_path):
        # 读取已保存的模型
        with open(model_path, "rb") as f:
            model_dic = pickle.load(f)  # noqa: S301

        conv_get = model_dic.get("conv1")
        conv_get.append(model_dic.get("step_conv1"))
        size_p1 = model_dic.get("size_pooling1")
        bp1 = model_dic.get("num_bp1")
        bp2 = model_dic.get("num_bp2")
        bp3 = model_dic.get("num_bp3")
        r_w = model_dic.get("rate_weight")
        r_t = model_dic.get("rate_thre")
        # 创建模型实例
        conv_ins = CNN(conv_get, size_p1, bp1, bp2, bp3, r_w, r_t)
        # 修改模型参数
        conv_ins.w_conv1 = model_dic.get("w_conv1")
        conv_ins.wkj = model_dic.get("wkj")
        conv_ins.vji = model_dic.get("vji")
        conv_ins.thre_conv1 = model_dic.get("thre_conv1")
        conv_ins.thre_bp2 = model_dic.get("thre_bp2")
        conv_ins.thre_bp3 = model_dic.get("thre_bp3")
        return conv_ins

    def sig(self, x):
        return 1 / (1 + np.exp(-1 * x))

    def do_round(self, x):
        return round(x, 3)

    def convolute(self, data, convs, w_convs, thre_convs, conv_step):
        # 卷积过程
        size_conv = convs[0]
        num_conv = convs[1]
        size_data = np.shape(data)[0]
        # 获取原始图像数据的数据切片 data_focus
        data_focus = []
        for i_focus in range(0, size_data - size_conv + 1, conv_step):
            for j_focus in range(0, size_data - size_conv + 1, conv_step):
                focus = data[
                    i_focus : i_focus + size_conv, j_focus : j_focus + size_conv
                ]
                data_focus.append(focus)
        # 计算每个卷积核的特征图，并保存为矩阵列表
        data_featuremap = []
        size_feature_map = int((size_data - size_conv) / conv_step + 1)
        for i_map in range(num_conv):
            featuremap = []
            for i_focus in range(len(data_focus)):
                net_focus = (
                    np.sum(np.multiply(data_focus[i_focus], w_convs[i_map]))
                    - thre_convs[i_map]
                )
                featuremap.append(self.sig(net_focus))
            featuremap = np.asmatrix(featuremap).reshape(
                size_feature_map, size_feature_map
            )
            data_featuremap.append(featuremap)

        # 将数据切片展开为一维
        focus1_list = []
        for each_focus in data_focus:
            focus1_list.extend(self.Expand_Mat(each_focus))
        focus_list = np.asarray(focus1_list)
        return focus_list, data_featuremap

    def pooling(self, featuremaps, size_pooling, pooling_type="average_pool"):
        # 池化过程
        size_map = len(featuremaps[0])
        size_pooled = int(size_map / size_pooling)
        featuremap_pooled = []
        for i_map in range(len(featuremaps)):
            feature_map = featuremaps[i_map]
            map_pooled = []
            for i_focus in range(0, size_map, size_pooling):
                for j_focus in range(0, size_map, size_pooling):
                    focus = feature_map[
                        i_focus : i_focus + size_pooling,
                        j_focus : j_focus + size_pooling,
                    ]
                    if pooling_type == "average_pool":
                        # 平均池化
                        map_pooled.append(np.average(focus))
                    elif pooling_type == "max_pooling":
                        # 最大池化
                        map_pooled.append(np.max(focus))
            map_pooled = np.asmatrix(map_pooled).reshape(size_pooled, size_pooled)
            featuremap_pooled.append(map_pooled)
        return featuremap_pooled

    def _expand(self, data):
        # 将三维数据展开为一维列表
        data_expanded = []
        for i in range(len(data)):
            shapes = np.shape(data[i])
            data_listed = data[i].reshape(1, shapes[0] * shapes[1])
            data_listed = data_listed.getA().tolist()[0]
            data_expanded.extend(data_listed)
        data_expanded = np.asarray(data_expanded)
        return data_expanded

    def _expand_mat(self, data_mat):
        # 将矩阵展开为一维列表
        data_mat = np.asarray(data_mat)
        shapes = np.shape(data_mat)
        data_expanded = data_mat.reshape(1, shapes[0] * shapes[1])
        return data_expanded

    def _calculate_gradient_from_pool(
        self, out_map, pd_pool, num_map, size_map, size_pooling
    ):
        """
        根据池化层的数据切片计算梯度
        pd_pool: 矩阵列表
        out_map: 数据切片的形状（size_map*size_map）
        return: pd_all: 矩阵列表，[num, size_map, size_map]
        """
        pd_all = []
        i_pool = 0
        for i_map in range(num_map):
            pd_conv1 = np.ones((size_map, size_map))
            for i in range(0, size_map, size_pooling):
                for j in range(0, size_map, size_pooling):
                    pd_conv1[i : i + size_pooling, j : j + size_pooling] = pd_pool[
                        i_pool
                    ]
                    i_pool = i_pool + 1
            pd_conv2 = np.multiply(
                pd_conv1, np.multiply(out_map[i_map], (1 - out_map[i_map]))
            )
            pd_all.append(pd_conv2)
        return pd_all

    def train(
        self, patterns, datas_train, datas_teach, n_repeat, error_accuracy, draw_e=bool
    ):
        # 模型训练
        print("----------------------Start Training-------------------------")
        print((" - - Shape: Train_Data  ", np.shape(datas_train)))
        print((" - - Shape: Teach_Data  ", np.shape(datas_teach)))
        rp = 0
        all_mse = []
        mse = 10000
        while rp < n_repeat and mse >= error_accuracy:
            error_count = 0
            print(f"-------------Learning Time {rp}--------------")
            for p in range(len(datas_train)):
                # print('------------Learning Image: %d--------------'%p)
                data_train = np.asmatrix(datas_train[p])
                data_teach = np.asarray(datas_teach[p])
                data_focus1, data_conved1 = self.convolute(
                    data_train,
                    self.conv1,
                    self.w_conv1,
                    self.thre_conv1,
                    conv_step=self.step_conv1,
                )
                data_pooled1 = self.pooling(data_conved1, self.size_pooling1)
                shape_featuremap1 = np.shape(data_conved1)
                """
                print('  -----original shape   ', np.shape(data_train))
                print('  ---- after convolution  ',np.shape(data_conv1))
                print('  -----after pooling  ',np.shape(data_pooled1))
               """
                data_bp_input = self._expand(data_pooled1)
                bp_out1 = data_bp_input

                bp_net_j = np.dot(bp_out1, self.vji.T) - self.thre_bp2
                bp_out2 = self.sig(bp_net_j)
                bp_net_k = np.dot(bp_out2, self.wkj.T) - self.thre_bp3
                bp_out3 = self.sig(bp_net_k)

                # --------------模型学习------------------------
                # 计算误差和梯度---------------
                pd_k_all = np.multiply(
                    (data_teach - bp_out3), np.multiply(bp_out3, (1 - bp_out3))
                )
                pd_j_all = np.multiply(
                    np.dot(pd_k_all, self.wkj), np.multiply(bp_out2, (1 - bp_out2))
                )
                pd_i_all = np.dot(pd_j_all, self.vji)

                pd_conv1_pooled = pd_i_all / (self.size_pooling1 * self.size_pooling1)
                pd_conv1_pooled = pd_conv1_pooled.T.getA().tolist()
                pd_conv1_all = self._calculate_gradient_from_pool(
                    data_conved1,
                    pd_conv1_pooled,
                    shape_featuremap1[0],
                    shape_featuremap1[1],
                    self.size_pooling1,
                )
                # 权重和阈值的学习过程---------
                # 卷积层
                for k_conv in range(self.conv1[1]):
                    pd_conv_list = self._expand_mat(pd_conv1_all[k_conv])
                    delta_w = self.rate_weight * np.dot(pd_conv_list, data_focus1)

                    self.w_conv1[k_conv] = self.w_conv1[k_conv] + delta_w.reshape(
                        (self.conv1[0], self.conv1[0])
                    )

                    self.thre_conv1[k_conv] = (
                        self.thre_conv1[k_conv]
                        - np.sum(pd_conv1_all[k_conv]) * self.rate_thre
                    )
                # 全连接层
                self.wkj = self.wkj + pd_k_all.T * bp_out2 * self.rate_weight
                self.vji = self.vji + pd_j_all.T * bp_out1 * self.rate_weight
                self.thre_bp3 = self.thre_bp3 - pd_k_all * self.rate_thre
                self.thre_bp2 = self.thre_bp2 - pd_j_all * self.rate_thre
                # 计算所有单幅图像的误差总和
                errors = np.sum(abs(data_teach - bp_out3))
                error_count += errors
                # print('   ----Teach      ',data_teach)
                # print('   ----BP_output  ',bp_out3)
            rp = rp + 1
            mse = error_count / patterns
            all_mse.append(mse)

        def draw_error() -> None:
            yplot = [error_accuracy for i in range(int(n_repeat * 1.2))]
            plt.plot(all_mse, "+-")
            plt.plot(yplot, "r--")
            plt.xlabel("Learning Times")
            plt.ylabel("All_mse")
            plt.grid(True, alpha=0.5)
            plt.show()

        print("------------------Training Complete---------------------")
        print((" - - Training epoch: ", rp, f"     - - Mse: {mse:.6f}"))
        if draw_e:
            draw_error()
        return mse

    def predict(self, datas_test):
        # 模型预测
        produce_out = []
        print("-------------------Start Testing-------------------------")
        print((" - - Shape: Test_Data  ", np.shape(datas_test)))
        for p in range(len(datas_test)):
            data_test = np.asmatrix(datas_test[p])
            _data_focus1, data_conved1 = self.convolute(
                data_test,
                self.conv1,
                self.w_conv1,
                self.thre_conv1,
                conv_step=self.step_conv1,
            )
            data_pooled1 = self.pooling(data_conved1, self.size_pooling1)
            data_bp_input = self._expand(data_pooled1)

            bp_out1 = data_bp_input
            bp_net_j = bp_out1 * self.vji.T - self.thre_bp2
            bp_out2 = self.sig(bp_net_j)
            bp_net_k = bp_out2 * self.wkj.T - self.thre_bp3
            bp_out3 = self.sig(bp_net_k)
            produce_out.extend(bp_out3.getA().tolist())
        res = [list(map(self.do_round, each)) for each in produce_out]
        return np.asarray(res)

    def convolution(self, data):
        # 返回卷积后的图像数据，以便检查结果
        data_test = np.asmatrix(data)
        _data_focus1, data_conved1 = self.convolute(
            data_test,
            self.conv1,
            self.w_conv1,
            self.thre_conv1,
            conv_step=self.step_conv1,
        )
        data_pooled1 = self.pooling(data_conved1, self.size_pooling1)

        return data_conved1, data_pooled1


if __name__ == "__main__":
    """
    示例将放在另一个文件中
    """
