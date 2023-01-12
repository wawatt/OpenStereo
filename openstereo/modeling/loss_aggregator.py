"""The loss aggregator."""

from utils import Odict
from utils import get_ddp_module
from . import losses


# class LossAggregator():
#     """The loss aggregator.
#
#     This class is used to aggregate the losses.
#     For example, if you have two losses, one is triplet loss, the other is cross entropy loss,
#     you can aggregate them as follows:
#     loss_num = tripley_loss + cross_entropy_loss
#
#     Attributes:
#         losses: A dict of losses.
#     """
#
#     def __init__(self, loss_cfg) -> None:
#         """
#         Initialize the loss aggregator.
#
#         Args:
#             loss_cfg: Config of losses. List for multiple losses.
#         """
#         self.losses = {loss_cfg['log_prefix']: self._build_loss_(loss_cfg)} if is_dict(loss_cfg) \
#             else {cfg['log_prefix']: self._build_loss_(cfg) for cfg in loss_cfg}
#
#     def _build_loss_(self, loss_cfg):
#         """Build the losses from loss_cfg.
#
#         Args:
#             loss_cfg: Config of loss.
#         """
#         Loss = get_attr_from([losses], loss_cfg['type'])
#         valid_loss_arg = get_valid_args(
#             Loss, loss_cfg, ['type', 'gather_and_scale'])
#         loss = get_ddp_module(Loss(**valid_loss_arg).cuda())
#         return loss
#
#     def __call__(self, training_feats):
#         """Compute the sum of all losses.
#
#         The input is a dict of features. The key is the name of loss and the value is the feature and label. If the key not in
#         built losses and the value is torch.Tensor, then it is the computed loss to be added loss_sum.
#
#         Args:
#             training_feats: A dict of features. The same as the output["training_feat"] of the model.
#         """
#         loss_sum = .0
#         loss_info = Odict()
#
#         for k, v in training_feats.items():
#             if k in self.losses:
#                 loss_func = self.losses[k]
#                 loss, info = loss_func(**v)
#                 for name, value in info.items():
#                     loss_info['scalar/%s/%s' % (k, name)] = value
#                 loss = loss.mean() * loss_func.loss_term_weight
#                 loss_sum += loss
#
#             else:
#                 if isinstance(v, dict):
#                     raise ValueError(
#                         "The key %s in -Trainng-Feat- should be stated as the log_prefix of a certain loss defined in your loss_cfg."%v
#                     )
#                 elif is_tensor(v):
#                     _ = v.mean()
#                     loss_info['scalar/%s' % k] = _
#                     loss_sum += _
#                     get_msg_mgr().log_debug(
#                         "Please check whether %s needed in training." % k)
#                 else:
#                     raise ValueError(
#                         "Error type for -Trainng-Feat-, supported: A feature dict or loss tensor.")
#
#         return loss_sum, loss_info


class LossAggregator():
    """The loss aggregator.

    This class is used to aggregate the losses.
    For example, if you have two losses, one is triplet loss, the other is cross entropy loss,
    you can aggregate them as follows:
    loss_num = tripley_loss + cross_entropy_loss

    Attributes:
        losses: A dict of losses.
    """

    def __init__(self, loss_cfg) -> None:
        """
        Initialize the loss aggregator.

        Args:
            loss_cfg: Config of losses. List for multiple losses.
        """
        self.losses = {"Weighted_Smooth_l1_Loss": self._build_loss_(loss_cfg)}

    def _build_loss_(self, loss_cfg):
        """Build the losses from loss_cfg.

        Args:
            loss_cfg: Config of loss.
        """
        loss = losses.Weighted_Smooth_l1_Loss()
        loss = get_ddp_module(loss.cuda())

        # # Loss = get_attr_from([losses], loss_cfg['type'])
        # valid_loss_arg = get_valid_args(
        #     Loss, loss_cfg, ['type', 'gather_and_scale'])
        # loss = get_ddp_module(Loss(**valid_loss_arg).cuda())
        return loss

    def __call__(self, training_output):
        """Compute the sum of all losses.

        The input is a dict of features. The key is the name of loss and the value is the feature and label. If the key not in
        built losses and the value is torch.Tensor, then it is the computed loss to be added loss_sum.

        Args:
            training_feats: A dict of features. The same as the output["training_feat"] of the model.
        """
        # loss_sum = .0
        training_disp = training_output['training_disp']
        loss_info = Odict()

        pred_disp = training_disp['disp']
        gt_disp = training_disp['gt_disp']
        mask = training_disp['mask']
        middle = training_disp['middle_disp']
        # print(middle + [pred_disp])
        # print(gt_disp.shape)
        # print(mask.shape)
        loss = self.losses["Weighted_Smooth_l1_Loss"](middle + [pred_disp], gt_disp, mask)
        loss_info['scalar/Weighted_Smooth_l1_Loss'] = loss

        # for k, v in training_feats.items():
        #     if k in self.losses:
        #         loss_func = self.losses[k]
        #         loss, info = loss_func(**v)
        #         for name, value in info.items():
        #             loss_info['scalar/%s/%s' % (k, name)] = value
        #         loss = loss.mean() * loss_func.loss_term_weight
        #         loss_sum += loss
        #
        #     else:
        #         if isinstance(v, dict):
        #             raise ValueError(
        #                 "The key %s in -Trainng-Feat- should be stated as the log_prefix of a certain loss defined in your loss_cfg."%v
        #             )
        #         elif is_tensor(v):
        #             _ = v.mean()
        #             loss_info['scalar/%s' % k] = _
        #             loss_sum += _
        #             get_msg_mgr().log_debug(
        #                 "Please check whether %s needed in training." % k)
        #         else:
        #             raise ValueError(
        #                 "Error type for -Trainng-Feat-, supported: A feature dict or loss tensor.")

        return loss, loss_info
