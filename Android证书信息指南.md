# Android证书信息指南 - 声音贝壳(Shell Voice)应用

## 应用基本信息
- **应用名称**: 声音贝壳 (Shell Voice)
- **公司域名**: chatoffer.tech
- **软件包名称(Package Name)**: tech.chatoffer.shellvoice

## 证书信息
完成以下步骤后，请将实际获取的信息填写到下方：

### 证书MD5指纹
```
MD5指纹: ________________________________
```
(从keystore信息中复制实际的MD5指纹值)

### 公钥信息
公钥已保存在: `android_certificates/shellvoice_android_public_key.txt`

## 获取步骤指南

### 1. 创建Keystore文件
如果您还没有创建Keystore，请按照以下步骤创建：

```bash
keytool -genkey -v -keystore shellvoice.keystore -alias shellvoice -keyalg RSA -keysize 2048 -validity 10000
```

系统会提示您输入密码和一些信息，请妥善保存这些信息。

### 2. 获取证书MD5指纹
使用以下命令获取证书的MD5指纹：

```bash
keytool -list -v -keystore shellvoice.keystore -alias shellvoice
```

系统会要求您输入Keystore密码，然后显示证书信息，包括MD5指纹。

### 3. 获取应用公钥
从Google Play Console获取公钥：
1. 登录[Google Play Console](https://play.google.com/console/)
2. 选择您的应用
3. 进入"设置" > "应用签名"
4. 在"应用签名密钥证书"部分，您可以找到应用的公钥

或者使用以下命令从Keystore提取公钥：

```bash
keytool -exportcert -alias shellvoice -keystore shellvoice.keystore | openssl sha1 -binary | openssl base64
```

## 上架检查清单
- [ ] 已创建并记录软件包名称(Package Name)
- [ ] 已创建Keystore文件并妥善保存
- [ ] 已获取并记录证书MD5指纹
- [ ] 已获取并保存应用公钥
- [ ] 已在build.gradle中配置正确的签名信息

*注意：请妥善保管这些信息，特别是Keystore文件和密码，不要分享给未授权人员。如果丢失，您将无法更新应用。*
