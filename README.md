# 全景图拆分工具

一个用于辅助**混元 World-Mirror** 处理全景图的工具。可以将等距矩形投影（equirectangular）全景图拆分成标准的透视视角图片，这些标准视图可以作为输入提供给 World-Mirror 来生成全景场景。

## 🎯 用途说明

本工具主要用于 **混元 World-Mirror** 工作流程：
1. **输入**：等距矩形投影全景图（equirectangular format）
2. **处理**：将全景图拆分成多个标准透视视角（1-72.jpg）
3. **输出**：标准视图序列供 World-Mirror 使用，生成全景场景

生成的视图采用连续编号（1-72.jpg），包含仰头、平视、低头三个水平旋转圈，每圈 24 张图片，完全覆盖 360° 水平视角。

## ✨ 功能特点

- 🎥 **3圈水平旋转**：自动生成仰头、平视、低头三个视角的水平旋转序列
- 📐 **广角视角**：使用 130°×120° 视场角，提供更广阔的视野
- 🔄 **360° 全覆盖**：每圈生成 24 张图片（每 15° 一张），完整覆盖水平视角
- 🖼️ **标准命名**：输出文件按 1-72.jpg 连续编号，符合 World-Mirror 输入要求
- 💻 **多种运行方式**：支持命令行参数和交互式模式
- 🤖 **World-Mirror 专用**：针对混元 World-Mirror 场景生成优化

## 📋 依赖要求

### 必需依赖

- **Python 3.6+**（仅使用标准库，无需额外安装 Python 包）
- **FFmpeg**（需要单独安装并添加到系统 PATH）

### FFmpeg 安装

#### Windows

1. **方法一：使用 winget（推荐）**
   ```powershell
   winget install -e --id FFmpeg.FFmpeg
   ```

2. **方法二：手动安装**
   - 访问 [FFmpeg 官网](https://ffmpeg.org/download.html)
   - 下载 Windows 版本（推荐 [Gyan.dev 构建版](https://www.gyan.dev/ffmpeg/builds/)）
   - 解压到 `C:\ffmpeg`
   - 将 `C:\ffmpeg\bin` 添加到系统环境变量 PATH

3. **验证安装**
   ```cmd
   ffmpeg -version
   ```

#### macOS

```bash
# 使用 Homebrew
brew install ffmpeg
```

#### Linux

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg
```

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/YImingZHANG615/Equirectangular_Panorama_Splitter.git
cd Equirectangular_Panorama_Splitter

# 安装 Python 依赖（本工具仅使用标准库，此步骤为可选）
pip install -r requirements.txt

# 确保 FFmpeg 已安装（必需）
# FFmpeg 安装方法见上方的"FFmpeg 安装"章节
```

### 使用方法

#### 1. 命令行模式（推荐）

```bash
python panorama_split.py 全景图.jpg
```

**自定义参数：**

```bash
python panorama_split.py 全景图.jpg \
    --width 1920 \
    --height 1080 \
    --quality 2 \
    --h-fov 130 \
    --v-fov 120
```

**参数说明：**

| 参数 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `--width` | `-w` | 1280 | 输出图片宽度（像素） |
| `--height` | | 720 | 输出图片高度（像素） |
| `--quality` | `-q` | 2 | JPEG 质量（1-10，1=最高） |
| `--h-fov` | | 130 | 水平视场角（度） |
| `--v-fov` | | 120 | 垂直视场角（度） |

#### 2. 交互式模式

```bash
python panorama_split.py -i
# 或
python panorama_split.py --interactive
```

交互模式会引导你：
- 输入全景图路径
- 选择使用默认参数或自定义参数
- 可以连续处理多张图片

## 📊 输出说明

### 输出目录结构

```
output/
└── 输入文件名/
    ├── 1.jpg    # 仰头30° - yaw=0°
    ├── 2.jpg    # 仰头30° - yaw=15°
    ├── ...
    ├── 24.jpg   # 仰头30° - yaw=345°
    ├── 25.jpg   # 平视0° - yaw=0°
    ├── 26.jpg   # 平视0° - yaw=15°
    ├── ...
    ├── 48.jpg   # 平视0° - yaw=345°
    ├── 49.jpg   # 低头30° - yaw=0°
    ├── ...
    └── 72.jpg   # 低头30° - yaw=345°
```

### 输出规格

- **总数量**：72 张（3圈 × 24张）
- **命名规则**：连续编号 1-72.jpg
- **图片分组**：
  - 1-24.jpg：仰头 30° 水平旋转（pitch=30°）
  - 25-48.jpg：平视水平旋转（pitch=0°）
  - 49-72.jpg：低头 30° 水平旋转（pitch=-30°）

## 🎯 应用场景

- 🤖 **混元 World-Mirror**：为 World-Mirror 准备标准视图输入，生成全景场景（主要用途）
- 🎬 **视频制作**：全景图转视频序列，制作运镜效果
- 🎮 **游戏开发**：全景环境图切分为多视角预览图
- 🏗️ **建筑可视化**：全景漫游关键帧提取
- 📱 **VR/AR 内容**：全景素材预处理

## ⚙️ 技术参数

### 默认视角设置

| 参数 | 数值 | 说明 |
|------|------|------|
| 输出分辨率 | 1280×720 | HD 分辨率 |
| 水平 FOV | 130° | 模拟广角镜头 |
| 垂直 FOV | 120° | 更广的垂直视角 |
| 仰头角度 | +30° | pitch 正数表示向上 |
| 低头角度 | -30° | pitch 负数表示向下 |
| 水平步进 | 15° | 每圈 24 张（360°÷15°） |

### FFmpeg 滤镜参数

本工具使用 FFmpeg 的 `v360` 滤镜：
- **输入格式**：`equirect`（等距矩形投影）
- **输出格式**：`rectilinear`（透视投影）
- **投影参数**：`yaw`（水平旋转）、`pitch`（垂直角度）、`roll`（滚转，固定为 0）

## 📝 使用示例

### 示例 1：为 World-Mirror 准备标准视图（推荐）

```bash
python panorama_split.py panorama.jpg
```

生成 72 张标准视图（1-72.jpg）到 `output/panorama/` 目录，可直接输入到混元 World-Mirror 生成全景场景。

### 示例 2：高质量输出

```bash
python panorama_split.py panorama.jpg \
    --width 3840 \
    --height 2160 \
    --quality 1
```

生成 4K 分辨率、最高质量的图片。

### 示例 3：批量处理

在交互模式下，可以连续处理多张全景图：

```bash
python panorama_split.py -i
```

## 🐛 常见问题

### Q: 提示 "未找到 FFmpeg"？

**A:** 确保 FFmpeg 已正确安装并添加到系统 PATH：
- Windows: 检查环境变量中是否包含 FFmpeg 的 bin 目录
- 运行 `ffmpeg -version` 验证安装

### Q: 输出图片有变形或黑边？

**A:** 检查输入全景图是否为标准等距矩形投影（宽高比 2:1），例如 4096×2048 或 8192×4096。

### Q: 想要调整仰头/低头的角度？

**A:** 编辑 `panorama_split.py` 第 149 行：
```python
pitch_angles = [30, 0, -30]  # 改为 [45, 0, -45] 或其他角度
```

### Q: 想要更多圈数？

**A:** 修改第 149-150 行，例如生成 5 圈：
```python
pitch_angles = [60, 30, 0, -30, -60]
start_numbers = [1, 25, 49, 73, 97]
```

### Q: 处理速度慢？

**A:** 
- 降低输出分辨率（如 960×540）
- 使用 SSD 硬盘
- 减少生成的图片数量（增大角度步进）

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

FFmpeg 使用 LGPL/GPL 许可证，请确保遵守其许可证要求。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📧 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 [Issue](https://github.com/YImingZHANG615/Equirectangular_Panorama_Splitter/issues)
- 发送邮件：yimingarchitect@gmail.com

## 🙏 致谢

- [FFmpeg](https://ffmpeg.org/) - 强大的多媒体处理框架
- v360 滤镜 - FFmpeg 的全景投影转换滤镜

---

**如果这个项目对你有帮助，请给个 ⭐ Star！**


