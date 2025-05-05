#!/bin/bash

# 声音贝壳(Shell Voice)应用证书信息更新脚本

echo "声音贝壳(Shell Voice)应用证书信息更新工具"
echo "=========================================="
echo ""

# 获取SHA-1指纹
echo "请输入证书的SHA-1指纹 (格式如 AA:BB:CC:DD:...):"
read sha1_fingerprint

# 更新证书信息文件
if [ -n "$sha1_fingerprint" ]; then
    # 使用sed替换SHA-1行
    sed -i '' "s/SHA-1: .*/SHA-1: $sha1_fingerprint/" shellvoice_certificate_info.txt
    echo "SHA-1指纹已更新到 shellvoice_certificate_info.txt"
else
    echo "未输入SHA-1指纹，文件未更新"
fi

echo ""
echo "如果您有新的公钥文件，请将其复制到 shellvoice_public_key.pem 覆盖示例文件"
echo ""
echo "完成！"
