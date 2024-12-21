# 

## 
```shell
cd stereo/modeling/models/nmrf/ops 
python setup.py build install
```

## download swin_tiny_patch4_window7_224.pth
https://gitcode.com/open-source-toolkit/9fbf3/overview

## run infer
```powershell
python tools/infer.py --cfg_file cfgs/nmrf/nmrf_swint_sceneflow.yaml `
--pretrained_model checkpoints/stereoanything.pt `
--left_img_path demos/L.png `
--right_img_path demos/R.png `
--savename demos/res.png
```

## export
```
python deploy/export.py `
--config cfgs/nmrf/nmrf_swint_sceneflow.yaml `
--weights checkpoints/stereoanything.pt `
--device 0 `
--simplify --half --include onnx
```

```
python deploy/export.py --config cfgs/psmnet/psmnet_kitti.yaml --weights checkpoints\PSMNet_KITTI15_epoch_1000.pt --device 0 --simplify --half false --include onnx
```
```shell
python deploy/export.py --config cfgs/lightstereo/lightstereo_s_sceneflow.yaml --weights checkpoints/LightStereo-S-SceneFlow.ckpt --device 0 --simplify --half --include onnx
```
