from collections import namedtuple
# This is to be understood as a transition: Given `state0`, performing `action`
# yields `reward` and results in `state1`, which might be `terminal`.
# NOTE: used as the return format for Env(), and as the format to push into replay memory for off-policy methods (DQN)
# NOTE: when return from Env(), state0 is always None
Experience = namedtuple('Experience', 'state0, action, reward, state1, terminal1')

def reset_experience():
    return Experience(state0 = None,
                      action = None,
                      reward = None,
                      state1 = None,
                      terminal1 = False)


# target model
def update_target_model(model, target_model, target_model_update=1.):
    if target_model_update >= 1.:   # hard update
        target_model.load_state_dict(model.state_dict())
    else:                           # soft update
        for target_param, param in zip(target_model.parameters(), model.parameters()):
            target_param.data.copy_(target_param.data * (1. - target_model_update) +
                                    param.data * target_model_update)


def ensure_global_grads(local_model, global_model, global_device):
    for local_param, global_param in zip(local_model.parameters(),
                                         global_model.parameters()):
        if global_param.grad is not None:
            return
        global_param._grad = local_param.grad.to(global_device)
