#!/bin/bash

# 声音贝壳(Shell Voice)应用Android证书信息更新脚本

echo "声音贝壳(Shell Voice)应用Android证书信息更新工具"
echo "================================================"
echo ""

# 获取MD5指纹
echo "请输入证书的MD5指纹 (格式如 AA:BB:CC:DD:...):"
read md5_fingerprint

# 获取公钥
echo "请输入应用的公钥 (从Google Play Console获取):"
read public_key

# 更新证书信息文件
if [ -n "$md5_fingerprint" ]; then
    # 使用sed替换MD5行
    sed -i '' "s/MD5: .*/MD5: $md5_fingerprint/" shellvoice_android_certificate_info.txt
    echo "MD5指纹已更新到 shellvoice_android_certificate_info.txt"
else
    echo "未输入MD5指纹，MD5信息未更新"
fi

# 更新公钥文件
if [ -n "$public_key" ]; then
    echo "$public_key" > shellvoice_android_public_key.txt
    echo "公钥已更新到 shellvoice_android_public_key.txt"
else
    echo "未输入公钥，公钥文件未更新"
fi

echo ""
echo "如果您有Keystore文件，请将其复制到此目录并妥善保管"
echo ""
echo "完成！"
