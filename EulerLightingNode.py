

import numpy as np
from PIL import Image
import torch

class EulerLightingNode:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "diffuse_map": ("IMAGE",),
                "normal_map": ("IMAGE",),
                "specular_map": ("IMAGE",),
                "light_yaw": ("FLOAT", {"default": 45, "min": -180, "max": 180, "step": 1}),
                "light_pitch": ("FLOAT", {"default": 30, "min": -90, "max": 90, "step": 1}),
                "specular_power": ("FLOAT", {"default": 32, "min": 1, "max": 200, "step": 1}),
                "ambient_light": ("FLOAT", {"default": 0.50, "min": 0, "max": 1, "step": 0.01}),
                "NormalDiffuseStrength": ("FLOAT", {"default": 1.00, "min": 0, "max": 5.0, "step": 0.01}),
                "SpecularHighlightsStrength": ("FLOAT", {"default": 1.00, "min": 0, "max": 5.0, "step": 0.01}),
                "TotalGain": ("FLOAT", {"default": 1.00, "min": 0, "max": 2.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("IMAGE",)

    FUNCTION = "execute"
    CATEGORY = "custom"

    def execute(self, diffuse_map, normal_map, specular_map, light_yaw, light_pitch, specular_power, ambient_light,NormalDiffuseStrength,SpecularHighlightsStrength,TotalGain):

        # 入力画像をテンソルに変換
        diffuse_tensor = diffuse_map.permute(0, 3, 1, 2)  # (1, 512, 512, 3) -> (1, 3, 512, 512)
        normal_tensor = normal_map.permute(0, 3, 1, 2) * 2.0 - 1.0   # (1, 512, 512, 3) -> (1, 3, 512, 512)
        specular_tensor = specular_map.permute(0, 3, 1, 2)  # (1, 512, 512, 3) -> (1, 3, 512, 512)

        # 法線ベクトルを正規化
        normal_tensor = torch.nn.functional.normalize(normal_tensor, dim=1)

        # light_directionをブロードキャスト用に正しくリシェイプ
        light_direction = self.euler_to_vector(light_yaw, light_pitch, 0 )
        light_direction = light_direction.view(1, 3, 1, 1)  # [1, 3, 1, 1]にリシェイプしてブロードキャストを可能にする

        # camera_directionをブロードキャスト用に正しくリシェイプ
        camera_direction = self.euler_to_vector(0,0,0)
        camera_direction = camera_direction.view(1, 3, 1, 1) # [1, 3, 1, 1]にリシェイプしてブロードキャストを可能にする

        # 乗算のための既存のコード...
        diffuse = torch.sum(normal_tensor * light_direction, dim=1, keepdim=True)
        diffuse = torch.clamp(diffuse, 0, 1)

        # 鏡面反射の計算
        half_vector = torch.nn.functional.normalize(light_direction + camera_direction, dim=1)
        specular = torch.sum(normal_tensor * half_vector, dim=1, keepdim=True)
        specular = torch.pow(torch.clamp(specular, 0, 1), specular_power)

        # 拡散反射と鏡面反射の結果を合成
        output_tensor = ( diffuse_tensor * (ambient_light + diffuse * NormalDiffuseStrength ) + specular_tensor * specular * SpecularHighlightsStrength) * TotalGain

        # テンソルを出力用の画像に変換
        output_tensor = output_tensor.permute(0, 2, 3, 1)  # (1, 3, 512, 512) -> (1, 512, 512, 3)

        return (output_tensor,)


    def euler_to_vector(self, yaw, pitch, roll):
        yaw_rad = np.radians(yaw)
        pitch_rad = np.radians(pitch)
        roll_rad = np.radians(roll)

        cos_pitch = np.cos(pitch_rad)
        sin_pitch = np.sin(pitch_rad)
        cos_yaw = np.cos(yaw_rad)
        sin_yaw = np.sin(yaw_rad)
        cos_roll = np.cos(roll_rad)
        sin_roll = np.sin(roll_rad)

        direction = np.array([
            sin_yaw * cos_pitch,
            sin_pitch,
            cos_pitch * cos_yaw
        ])


        return torch.from_numpy(direction).float()

    def convert_tensor_to_image(self, tensor):
        # PyTorchのテンソルをPIL.Imageに変換
        tensor = tensor.squeeze(0)  # (1, 512, 512, 3) -> (512, 512, 3)
        tensor = tensor.clamp(0, 1)  # テンソルの値を0から1の範囲に制限
        image = Image.fromarray((tensor.detach().cpu().numpy() * 255).astype(np.uint8))
        return image


        
NODE_CLASS_MAPPINGS = {
    "EulerLightingNode": EulerLightingNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EulerLightingNode": "NormalLighting"
}



