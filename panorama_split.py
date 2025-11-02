#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全景图拆分工具 - Python 版本
支持交互式输入，自动处理全景图为多个视角
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import argparse


class PanoramaSplitter:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.ffmpeg_path = self.script_dir / "ffmpeg" / "bin" / "ffmpeg.exe"
        self.default_width = 1280
        self.default_height = 720
        self.default_quality = 2
        self.default_h_fov = 130
        self.default_v_fov = 120  # 垂直视场角（更广的视角）
        
    def check_ffmpeg(self):
        """检查FFmpeg是否可用"""
        if self.ffmpeg_path.exists():
            return str(self.ffmpeg_path)
        
        # 检查系统PATH中的ffmpeg
        if shutil.which("ffmpeg"):
            return "ffmpeg"
            
        print("❌ 错误: 未找到 FFmpeg")
        print("请确保:")
        print("1. 项目目录下有 ffmpeg/bin/ffmpeg.exe")
        print("2. 或系统PATH中有 ffmpeg")
        return None
    
    def validate_input_file(self, file_path):
        """验证输入文件"""
        path = Path(file_path)
        if not path.exists():
            return False, f"文件不存在: {file_path}"
        
        if path.suffix.lower() not in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
            return False, f"不支持的文件格式: {path.suffix}"
        
        return True, str(path.resolve())
    
    def create_output_dir(self, input_path):
        """创建输出目录"""
        input_name = Path(input_path).stem
        output_dir = self.script_dir / "output" / input_name
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir
    
    def run_ffmpeg(self, ffmpeg_cmd, input_file, filter_str, output_file, quality):
        """运行FFmpeg命令"""
        cmd = [
            ffmpeg_cmd, "-y", "-loglevel", "error",
            "-i", input_file,
            "-vf", filter_str,
            "-q:v", str(quality),
            output_file
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                print(f"⚠️  FFmpeg错误: {result.stderr.strip()}")
                return False
            return True
        except subprocess.TimeoutExpired:
            print("⚠️  FFmpeg超时")
            return False
        except Exception as e:
            print(f"⚠️  执行错误: {e}")
            return False
    
    def generate_horizontal_circle(self, ffmpeg_cmd, input_file, output_dir, 
                                 width, height, quality, h_fov, v_fov, pitch=0, start_number=1):
        """生成水平一圈 (24张，每15°)"""
        pitch_name = "平视" if pitch == 0 else ("仰头" if pitch > 0 else "低头")
        print(f"🔄 生成水平一圈 - {pitch_name} (pitch={pitch:+.0f}°, 24张，每15°)...")
        
        success_count = 0
        angles = list(range(0, 360, 15))  # 0, 15, 30, ..., 345
        
        for i, yaw in enumerate(angles):
            # 映射yaw到[-180, 180]范围
            mapped_yaw = yaw if yaw <= 180 else yaw - 360
            
            filter_str = f"v360=input=equirect:output=rectilinear:h_fov={h_fov}:v_fov={v_fov}:yaw={mapped_yaw}:pitch={pitch}:roll=0:w={width}:h={height}"
            
            # 文件命名：使用连续编号
            file_number = start_number + i
            output_file = output_dir / f"{file_number}.jpg"
            
            print(f"   [{i+1:2d}/24] yaw={yaw:3d}°, pitch={pitch:+.0f}° → {output_file.name}")
            
            if self.run_ffmpeg(ffmpeg_cmd, input_file, filter_str, str(output_file), quality):
                success_count += 1
        
        print(f"✅ {pitch_name}圈完成: {success_count}/24 张 ({start_number}-{start_number+23}.jpg)")
        return success_count
    
    def process_panorama(self, input_file, width=None, height=None, quality=None, 
                        h_fov=None, v_fov=None):
        """处理全景图"""
        # 使用默认值
        width = width or self.default_width
        height = height or self.default_height
        quality = quality or self.default_quality
        h_fov = h_fov or self.default_h_fov
        v_fov = v_fov or self.default_v_fov
        
        print("=" * 50)
        print("🌍 全景图拆分工具")
        print("=" * 50)
        
        # 检查FFmpeg
        ffmpeg_cmd = self.check_ffmpeg()
        if not ffmpeg_cmd:
            return False
        
        # 验证输入文件
        valid, result = self.validate_input_file(input_file)
        if not valid:
            print(f"❌ {result}")
            return False
        
        input_file = result
        print(f"📁 输入文件: {Path(input_file).name}")
        
        # 创建输出目录
        output_dir = self.create_output_dir(input_file)
        print(f"📁 输出目录: {output_dir}")
        
        # 显示参数
        print(f"⚙️  参数: {width}×{height}, 质量={quality}, FOV={h_fov}°×{v_fov}°")
        print()
        
        # 生成3圈水平旋转：
        # 第1圈：仰头一点 (pitch>0) 水平转一圈 → 1-24.jpg
        # 第2圈：平视 (pitch=0) 水平转一圈 → 25-48.jpg
        # 第3圈：低头一点 (pitch<0) 水平转一圈 → 49-72.jpg
        pitch_angles = [30, 0, -30]  # 仰头一点、平视、低头一点
        start_numbers = [1, 25, 49]  # 每圈的起始编号
        total_count = 0
        
        for i, (pitch, start_num) in enumerate(zip(pitch_angles, start_numbers), 1):
            print(f"\n[{i}/3]", end=" ")
            count = self.generate_horizontal_circle(ffmpeg_cmd, input_file, output_dir,
                                                    width, height, quality, h_fov, v_fov, 
                                                    pitch, start_num)
            total_count += count
        
        print()
        print("=" * 50)
        print(f"🎉 处理完成!")
        print(f"📊 总计: {total_count}/72 张图片")
        print(f"   第1圈（仰头30°）: 1-24.jpg")
        print(f"   第2圈（平视0°）: 25-48.jpg")
        print(f"   第3圈（低头30°）: 49-72.jpg")
        print(f"📁 输出: {output_dir}")
        print("=" * 50)
        
        return total_count == 72
    
    def interactive_mode(self):
        """交互式模式"""
        print("🌍 全景图拆分工具 - 交互模式")
        print("=" * 50)
        
        while True:
            # 输入文件路径
            print("\n📁 请输入全景图路径:")
            print("   支持格式: .jpg, .jpeg, .png, .bmp, .tiff")
            print("   输入 'q' 退出")
            
            file_path = input("➤ 文件路径: ").strip().strip('"\'')
            
            if file_path.lower() == 'q':
                print("👋 再见!")
                break
            
            if not file_path:
                print("❌ 请输入有效路径")
                continue
            
            # 验证文件
            valid, result = self.validate_input_file(file_path)
            if not valid:
                print(f"❌ {result}")
                continue
            
            # 询问是否使用默认参数
            print(f"\n⚙️  默认参数: {self.default_width}×{self.default_height}, 质量={self.default_quality}, FOV={self.default_h_fov}°×{self.default_v_fov}°")
            use_default = input("使用默认参数? (Y/n): ").strip().lower()
            
            if use_default in ['', 'y', 'yes']:
                # 使用默认参数
                success = self.process_panorama(result)
            else:
                # 自定义参数
                try:
                    width = int(input(f"宽度 (默认{self.default_width}): ") or self.default_width)
                    height = int(input(f"高度 (默认{self.default_height}): ") or self.default_height)
                    quality = int(input(f"质量1-10 (默认{self.default_quality}): ") or self.default_quality)
                    h_fov = int(input(f"水平FOV (默认{self.default_h_fov}): ") or self.default_h_fov)
                    v_fov = int(input(f"垂直FOV (默认{self.default_v_fov}): ") or self.default_v_fov)
                    
                    success = self.process_panorama(result, width, height, quality, h_fov, v_fov)
                except ValueError:
                    print("❌ 参数格式错误，使用默认参数")
                    success = self.process_panorama(result)
            
            if success:
                print("✅ 处理成功!")
            else:
                print("❌ 处理失败!")
            
            # 询问是否继续
            continue_choice = input("\n继续处理其他图片? (Y/n): ").strip().lower()
            if continue_choice in ['n', 'no']:
                print("👋 再见!")
                break


def main():
    parser = argparse.ArgumentParser(description="全景图拆分工具")
    parser.add_argument("input", nargs="?", help="输入全景图路径")
    parser.add_argument("-w", "--width", type=int, default=1280, help="输出宽度")
    parser.add_argument("--height", type=int, default=720, help="输出高度")
    parser.add_argument("-q", "--quality", type=int, default=2, help="JPEG质量 (1-10)")
    parser.add_argument("--h-fov", type=int, default=130, help="水平视场角")
    parser.add_argument("--v-fov", type=int, default=120, help="垂直视场角")
    parser.add_argument("-i", "--interactive", action="store_true", help="交互模式")
    
    args = parser.parse_args()
    
    splitter = PanoramaSplitter()
    
    if args.interactive or not args.input:
        # 交互模式
        splitter.interactive_mode()
    else:
        # 命令行模式
        success = splitter.process_panorama(
            args.input, args.width, args.height, args.quality, 
            args.h_fov, args.v_fov
        )
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
