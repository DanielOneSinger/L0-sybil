#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试脚本 - 验证项目设置
"""

import os
import sys
import yaml

def test_imports():
    """测试模块导入"""
    print("测试模块导入...")
    
    try:
        import binance_api
        print("✓ binance_api 导入成功")
    except ImportError as e:
        print(f"✗ binance_api 导入失败: {e}")
    
    try:
        import lighter_api
        print("✓ lighter_api 导入成功")
    except ImportError as e:
        print(f"✗ lighter_api 导入失败: {e}")
    
    try:
        import arbitrage_engine
        print("✓ arbitrage_engine 导入成功")
    except ImportError as e:
        print(f"✗ arbitrage_engine 导入失败: {e}")

def test_config():
    """测试配置文件"""
    print("\n测试配置文件...")
    
    config_path = "config.yaml"
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # 检查必要的配置项
            required_sections = ['exchanges', 'strategy', 'logging']
            for section in required_sections:
                if section in config:
                    print(f"✓ {section} 配置存在")
                else:
                    print(f"✗ {section} 配置缺失")
            
            # 检查交易所配置
            exchanges = config.get('exchanges', {})
            if 'binance' in exchanges:
                print("✓ Binance 配置存在")
            else:
                print("✗ Binance 配置缺失")
            
            if 'lighter' in exchanges:
                print("✓ Lighter 配置存在")
            else:
                print("✗ Lighter 配置缺失")
                
        except Exception as e:
            print(f"✗ 配置文件读取失败: {e}")
    else:
        print(f"✗ 配置文件不存在: {config_path}")

def test_dependencies():
    """测试依赖包"""
    print("\n测试依赖包...")
    
    dependencies = [
        'aiohttp',
        'websockets', 
        'httpx',
        'pyyaml',
        'pycryptodome',
        'cryptography',
        'pynacl',
        'lighter'
    ]
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✓ {dep} 已安装")
        except ImportError:
            print(f"✗ {dep} 未安装")

def test_file_structure():
    """测试文件结构"""
    print("\n测试文件结构...")
    
    required_files = [
        'config.yaml',
        'main.py',
        'binance_api.py',
        'lighter_api.py',
        'arbitrage_engine.py',
        'requirements.txt',
        'README.md'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} 存在")
        else:
            print(f"✗ {file} 缺失")
    
    # 检查logs目录
    if os.path.exists('logs'):
        print("✓ logs 目录存在")
    else:
        print("✗ logs 目录缺失")

def main():
    """主测试函数"""
    print("Binance-Lighter 套利机器人项目测试")
    print("=" * 50)
    
    test_file_structure()
    test_config()
    test_dependencies()
    test_imports()
    
    print("\n" + "=" * 50)
    print("测试完成！")
    print("\n如果所有测试都通过，你可以运行以下命令启动机器人：")
    print("python main.py --test  # 测试模式")
    print("python main.py         # 正常运行")

if __name__ == "__main__":
    main() 