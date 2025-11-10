# 自定义域名配置指南 - northcloud.cloud

本指南专门针对 `northcloud.cloud` 域名的 Vercel 配置。

## 📋 快速配置步骤

### 1. 在 Vercel 中添加域名

1. 登录 [Vercel Dashboard](https://vercel.com/dashboard)
2. 选择你的项目
3. 进入 **Settings** → **Domains**
4. 在 "Add Domain" 输入框中输入：`northcloud.cloud`
5. 点击 **Add**

### 2. 配置 DNS 记录

Vercel 会显示需要配置的 DNS 记录。根据你的域名注册商，选择以下方式之一：

#### 方式 1: 使用 A 记录（推荐，兼容性最好）

在你的域名注册商（Namecheap、GoDaddy、Cloudflare 等）的 DNS 管理页面添加：

```
类型: A
主机记录: @ (或留空，表示根域名 northcloud.cloud)
记录值: 76.76.21.21 (Vercel 提供的 IP 地址，请查看 Vercel 显示的准确值)
TTL: 3600 (或自动)
```

**注意**: 如果 Vercel 显示多个 IP 地址，需要添加多条 A 记录。

#### 方式 2: 使用 CNAME 记录（如果支持）

```
类型: CNAME
主机记录: @ (或留空)
记录值: cname.vercel-dns.com (Vercel 提供的 CNAME，请查看 Vercel 显示的准确值)
TTL: 3600 (或自动)
```

**注意**: 某些域名注册商（如 Namecheap）不支持根域名的 CNAME，必须使用 A 记录。

#### 方式 3: 使用 ALIAS/ANAME 记录（如果支持）

如果你的域名注册商支持 ALIAS 或 ANAME 记录（如 Cloudflare、DNSimple）：

```
类型: ALIAS (或 ANAME)
主机记录: @
记录值: cname.vercel-dns.com
TTL: 3600
```

### 3. 常见域名注册商的配置方法

#### Namecheap

1. 登录 Namecheap 账户
2. 进入 **Domain List** → 选择 `northcloud.cloud`
3. 点击 **Advanced DNS**
4. 在 **Host Records** 部分添加：
   - **Type**: A Record
   - **Host**: @
   - **Value**: `76.76.21.21` (使用 Vercel 显示的 IP)
   - **TTL**: Automatic
5. 点击保存

#### Cloudflare

1. 登录 Cloudflare 账户
2. 选择 `northcloud.cloud` 域名
3. 进入 **DNS** → **Records**
4. 添加记录：
   - **Type**: A
   - **Name**: @
   - **IPv4 address**: `76.76.21.21` (使用 Vercel 显示的 IP)
   - **Proxy status**: DNS only (关闭代理，或使用 Proxied 也可以)
   - **TTL**: Auto
5. 保存

#### GoDaddy

1. 登录 GoDaddy 账户
2. 进入 **My Products** → **DNS**
3. 在 **Records** 部分添加：
   - **Type**: A
   - **Name**: @
   - **Value**: `76.76.21.21` (使用 Vercel 显示的 IP)
   - **TTL**: 1 Hour
4. 保存

### 4. 验证 DNS 配置

配置 DNS 后，等待 5-60 分钟让 DNS 记录生效。你可以：

1. **在 Vercel 中查看状态**
   - 返回 Vercel Dashboard → Settings → Domains
   - 查看 `northcloud.cloud` 的状态
   - 当显示 "Valid Configuration" 时，配置成功

2. **使用命令行检查**
   ```bash
   # 检查 A 记录
   dig northcloud.cloud A
   
   # 或使用 nslookup
   nslookup northcloud.cloud
   ```

3. **在线工具检查**
   - 访问 https://dnschecker.org
   - 输入 `northcloud.cloud`
   - 查看全球 DNS 解析情况

### 5. SSL 证书自动配置

Vercel 会自动为你的域名配置 SSL 证书：

- ✅ 自动申请 Let's Encrypt 证书
- ✅ 自动续期（无需手动操作）
- ✅ 支持 HTTPS 访问
- ⏱️ 通常需要 5-10 分钟完成配置

在 Vercel 的 Domains 页面可以看到 SSL 证书状态。

### 6. 验证访问

配置完成后，访问：

- ✅ `https://northcloud.cloud` - 应该正常访问
- ✅ `http://northcloud.cloud` - 会自动重定向到 HTTPS

## 🔧 常见问题排查

### Q1: DNS 验证一直失败

**检查清单**:
- [ ] DNS 记录是否正确配置（类型、值、主机记录）
- [ ] 是否等待足够的时间（至少 10-15 分钟）
- [ ] 域名是否解锁（关闭隐私保护）
- [ ] 是否使用了正确的 IP 地址（查看 Vercel 显示的准确值）

**解决方法**:
1. 删除旧的 DNS 记录，重新添加
2. 使用 `dig` 或 `nslookup` 检查 DNS 是否已生效
3. 联系域名注册商技术支持

### Q2: SSL 证书配置失败

**可能原因**:
- DNS 记录未正确配置
- 域名指向了错误的服务器

**解决方法**:
1. 确保 DNS 记录正确
2. 等待更长时间（最多 24 小时）
3. 在 Vercel 中手动重新验证域名

### Q3: 网站可以访问但显示不安全

**原因**: SSL 证书还在配置中

**解决方法**: 等待 5-10 分钟，Vercel 会自动完成 SSL 配置

### Q4: 某些地区无法访问

**可能原因**: DNS 传播未完成

**解决方法**: 
- 使用 https://dnschecker.org 检查全球 DNS 解析
- 等待 24-48 小时让 DNS 完全传播

## 📝 DNS 记录参考值

**重要**: 以下值仅供参考，请使用 Vercel Dashboard 中显示的准确值！

### Vercel A 记录（示例）
```
76.76.21.21
76.223.126.88
```

### Vercel CNAME 记录（示例）
```
cname.vercel-dns.com
```

**⚠️ 注意**: 实际值可能不同，请务必查看 Vercel 显示的准确值！

## 🎯 配置完成检查清单

- [ ] 在 Vercel 中添加了 `northcloud.cloud` 域名
- [ ] 在域名注册商配置了正确的 DNS 记录
- [ ] 等待 DNS 记录生效（5-60 分钟）
- [ ] Vercel 显示 "Valid Configuration"
- [ ] SSL 证书已配置完成
- [ ] 可以通过 `https://northcloud.cloud` 访问网站
- [ ] HTTP 自动重定向到 HTTPS

## 📞 需要帮助？

如果遇到问题：

1. **查看 Vercel 文档**: https://vercel.com/docs/concepts/projects/domains
2. **检查 Vercel Dashboard**: Settings → Domains 中的错误提示
3. **联系域名注册商**: 确认 DNS 配置是否正确
4. **Vercel 支持**: 在 Vercel Dashboard 中提交支持请求

---

**最后更新**: 2025-01  
**域名**: northcloud.cloud  
**部署平台**: Vercel

