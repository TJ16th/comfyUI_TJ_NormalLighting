# comfyUI_TJ_NormalLighting
Custom Node for comfyUI for virtual lighting based on normal map

## 日本語は英文の後ろにあります

<img src="https://github.com/TJ16th/comfyUI_TJ_NormalLighting/assets/30209833/56e023f7-3c9a-4dbe-87cb-5d8165f2ce9f" title="sphere">
https://github.com/TJ16th/comfyUI_TJ_NormalLighting/assets/30209833/6348c878-8f63-4f1f-a296-327e6c008acc

## Please read first

I love technology such as XR and AI, but I'm not a programming expert.
Also, this is my first time publishing my code on Github.
I don't know much about Github. So if I make a mistake, please smile and forgive me.

## Lighting model

This program calculates diffuse reflection based on the Lambert Reflection Model.

The Lambertian reflection model is one of the most basic models of diffuse reflection and has the following characteristics:

Assume that the surface is completely diffusive and the incident light is isotropically scattered.
The intensity of the reflected light is proportional to the dot product of the intensity of the incident light, the surface normal vector, and the direction vector of the light.
The intensity of reflected light does not depend on the position of the viewpoint.

In addition to diffuse reflection, we also use Phong's specular reflection model to calculate specular reflection.
The inner product of the half vector (intermediate vector between the direction of the light and the direction of the camera) and the normal vector is calculated and combined with the value of the specular map to find the intensity of specular reflection.

## How to use

### input

Please enter 3 images. Please keep the image sizes the same.
diffuse_map: normal RGB image
normal_map: Normal image. RGB images compatible with XYZ axes
specular_map: Specular map. It's RGB. Reflected light can be colored

### Parameters

#### Light source direction
light_yaw, light_pitch: Euler angle indicating the direction of the light source. The unit is Deg.

#### Strength of specular reflection
specular_power: A parameter that controls the strength of specular reflection. Physically, it expresses the smoothness and gloss of a surface.

The larger the value of specular_power, the stronger the specular reflection. Specifically, it has the following effects.

The larger the specular_power, the sharper the specular highlights. In other words, the range of highlights is narrower and you get a stronger shine.
The smaller the specular_power, the more spread out the specular highlights will be. This means you get a wider range of highlights and a softer glow.

If specular_power = 1, specular reflection is the same as Lambertian reflection (fully diffuse reflection).
If specular_power = 10 or so, you'll get relatively spread out highlights that look like plastic.
If specular_power = 100 or so, you will get sharp highlights like metal.

The value of specular_power varies depending on the material. Commonly used values include:
Plastic: 10~100
Metal: 100~1000
Shiny surface: 10~1000
Matte surface: 1-10
However, these are typical values and actual values will vary depending on the material and purpose.

#### Output balance
ambient_light: Does not depend on the direction of the light source. If set to 1, the input diffuse_map will be output as is.

NormalDiffuseStrength: Adjusts the strength of diffused light due to Lambertian reflection.

SpecularHighlightsStrength: Adjusts the specular reflections by Phong's specular reflection model.

TotalGain: Adjust the overall brightness.

The output is expressed by the following formula:

output_tensor = ( diffuse_tensor * (ambient_light + diffuse * NormalDiffuseStrength ) + specular_tensor * specular * SpecularHighlightsStrength) * TotalGain


# 日本語解説

ノーマルマップベースのバーチャルライティング機能を提供します。

私はXRやAIなどのTechnologyを愛していますが、プログラミングの専門家ではありません。
また、Githubで私のコードを公開するのは、これが初めてです。
Githubのことは詳しくない。なので、何か間違えたら笑って許してください。

## ライティングモデル

このプログラムでは、ランバート反射モデル（Lambert Reflection Model）に基づいて拡散反射の計算を行っています。

ランバート反射モデルは、拡散反射の最も基本的なモデルの1つであり、以下の特徴を持っています。

表面は完全に拡散性であり、入射光は等方的に散乱されると仮定します。
反射光の強度は、入射光の強度と表面法線ベクトルと光の方向ベクトルの内積に比例します。
反射光の強度は、視点の位置に依存しません。

また、拡散反射に加えて、フォン（Phong）の鏡面反射モデルを使用して鏡面反射の計算も行っています。
ハーフベクトル（光の方向とカメラの方向の中間ベクトル）とノーマルベクトルの内積を計算し、スペキュラーマップの値と組み合わせて鏡面反射の強度を求めています。

## 使い方

### 入力

3つの画像を入力してください。画像サイズは揃えてください。
diffuse_map:通常のRGB画像
normal_map:法線画像。XYZ軸に対応したRGB画像
specular_map:スペキュラーマップ。RGBです。反射光に色を付けられます

### パラメータ

#### 光源の向き
light_yaw, light_pitch: 光源の方位をしめすオイラー角です。単位はDeg。

#### 鏡面反射の強さ
specular_power: 鏡面反射の強さを制御するパラメータです。物理的には、表面の滑らかさや光沢度を表現します。

specular_powerの値が大きいほど、鏡面反射の強さが増加します。具体的には、以下のような効果があります。

specular_powerが大きいほど、鏡面反射のハイライトがより鋭くなります。つまり、ハイライトの範囲が狭くなり、より強い光沢感が得られます。
specular_powerが小さいほど、鏡面反射のハイライトがより広がります。つまり、ハイライトの範囲が広くなり、より柔らかい光沢感が得られます。

specular_power = 1の場合、鏡面反射はランバート反射（完全拡散反射）と同じになります。
specular_power = 10程度の場合、プラスチックのような比較的広がったハイライトが得られます。
specular_power = 100程度の場合、金属のような鋭いハイライトが得られます。

specular_powerの値は、材質によって異なります。一般的に、以下のような値が使用されます。
プラスチック: 10〜100
金属: 100〜1000
光沢のある表面: 10〜1000
光沢のない表面: 1〜10
ただし、これらは一般的な値であり、実際の値は材質や目的によって異なります。

#### 出力バランス
ambient_light: 光源の向きに依存しません。1にすると、入力したdiffuse_mapをそのまま出力します。

NormalDiffuseStrength: ランバート反射による拡散光の強さ調整を行います。

SpecularHighlightsStrength: フォン（Phong）の鏡面反射モデルによる鏡面反射の調整をします。

TotalGain: 全体の明るさを調整します。

出力は、以下の式で表されます。

output_tensor = ( diffuse_tensor * (ambient_light + diffuse * NormalDiffuseStrength ) + specular_tensor * specular * SpecularHighlightsStrength) * TotalGain


