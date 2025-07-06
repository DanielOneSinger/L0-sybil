# Lighter API密钥设置指南

## 概述

本指南介绍如何配置Lighter API密钥，实现自动初始化和管理。

## 配置步骤

### 1. 配置钱包私钥

在 `config.yaml` 文件中，找到 `exchanges.lighter` 部分，设置你的钱包私钥：

```yaml
exchanges:
  lighter:
    open: true
    base_url: "https://mainnet.zklighter.elliot.ai"
    wallet_private_key: "你的钱包私钥"  # 在这里填入你的钱包私钥
    api_key_private_key: ""  # 这个会在运行时自动生成
    account_index: 15686
    api_key_index: 1
    # ... 其他配置
```

### 2. 运行方式

#### 方式一：自动初始化（推荐）

直接运行主程序，系统会自动检测并初始化API密钥：

```bash
python main.py
```

#### 方式二：仅初始化API密钥

如果只想初始化API密钥而不运行套利机器人：

```bash
python main.py --init-only
```

#### 方式三：手动初始化

也可以单独运行初始化脚本：

```bash
python lighter_init.py
```

### 3. 初始化流程

1. **验证账户**：系统会验证你提供的钱包私钥对应的账户是否存在
2. **生成API密钥**：自动生成新的API私钥和公钥对
3. **更新服务器**：将新的API公钥上传到Lighter服务器
4. **保存配置**：将生成的API私钥保存到配置文件中
5. **验证连接**：测试API连接是否正常

### 4. 安全注意事项

- **钱包私钥安全**：确保你的钱包私钥安全，不要泄露给他人
- **配置文件权限**：确保配置文件只有你有读取权限
- **定期更新**：建议定期更新API密钥以提高安全性

### 5. 故障排除

#### 常见错误

1. **"钱包私钥未配置"**
   - 解决：在config.yaml中设置 `wallet_private_key`

2. **"账户未找到"**
   - 解决：确认钱包私钥正确，且该钱包在Lighter上有账户

3. **"生成API密钥失败"**
   - 解决：检查网络连接，确保能访问Lighter服务器

4. **"更新API密钥失败"**
   - 解决：确认钱包有足够的权限，网络连接正常

#### 调试模式

启用详细日志来调试问题：

```bash
python main.py --test
```

### 6. 配置文件示例

完整的Lighter配置示例：

```yaml
exchanges:
  lighter:
    open: true
    base_url: "https://mainnet.zklighter.elliot.ai"
    wallet_private_key: "0x1234567890abcdef..."  # 你的钱包私钥
    api_key_private_key: ""  # 自动生成，无需手动填写
    account_index: 15686  # 可选，系统会自动检测
    api_key_index: 1
    fees_percent:
      maker: 0.0001
      taker: 0.00035
    leverage: 10
```

### 7. 运行日志

初始化过程会在日志中记录详细信息，包括：

- 账户验证状态
- API密钥生成过程
- 服务器更新状态
- 连接测试结果

日志文件位置：`logs/arbitrage.log`

## 总结

通过以上配置，系统会在每次启动时自动检查并初始化Lighter API密钥，无需手动管理。只需要在配置文件中设置一次钱包私钥，后续运行都会自动处理API密钥的生成和更新。 