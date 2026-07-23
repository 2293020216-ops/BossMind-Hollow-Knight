# BossMind — 跨设备 Agent 交接提纲

> **用途**：两台设备上的 Agent / 开发者共用本文档传递上下文。  
> **维护规则**：每一轮开发结束后，**必须更新本文档**（尤其是「当前状态」「本轮变更」「下一步」）。  
> **原则**：代码靠 Git 同步；对话靠本文档接力。不要假设另一台机器看过本地聊天记录。

---

## 0. 更新协议（给所有 Agent）

每轮结束前按顺序做：

1. 更新 **§2 当前状态**（阶段、完成项、阻塞）
2. 重写 **§3 下一步**
3. 约定有变时改 **§1 / §4–§6**
4. **§8 项目日志**：只记里程碑（过验收、重要架构定稿、环境冒烟成败）；**不要**为改文档措辞、依赖微调等琐事追加日志
5. 提醒用户：`git add` / `commit` / `push`（若已用远程）

用户换设备后，新 Agent **先读本文档再动手**。

---

## 1. 项目一句话 & 硬约束

| 项 | 内容 |
|----|------|
| 项目 | BossMind：真空洞骑士单 Boss 分层 Agent（策略家 + 弱融合训练师） |
| 主线 | 真环境；BC 为主；RL 可选加深；LLM 选 Option + 局外门禁式自我改进 |
| 不做（当前阶段） | 通关全图、LLM 每帧按键、在线热更新权重、为简历硬融 RAG |
| 用户目标 | **自行实现**以提高工程能力；Agent 当师父：讲思路、审代码、排错，**不代写整份可粘贴完工代码**（除非用户明确要求生成某文件） |

### 双设备分工（以用户最终约定为准 — 必读）

**工作方式**：两台设备 **交替开发**（两边都可以写代码、开 Agent 对话）。能力不对称如下：

| 设备 | 强制环境 | 能做什么 | 不能做什么 |
|------|----------|----------|------------|
| **设备 A** | Windows 亦可 | 写代码、改逻辑、写文档、单测（无游戏）、Git、与 Agent 讨论设计 | **不能**作为空洞骑士运行/内存读/采集/评估的主环境；**不能**做 GPU 主训练 |
| **设备 B（7900 XT）** | **必须 Windows** | **也能写代码**；且负责跑 HK、内存读、按键、采集、固定存档评估、局内 play；同机 WSL2+ROCm 做 BC/CNN/可选 RL | — |

```text
交替开发（A 或 B 都可写代码）→ 随时 git push/pull 对齐

凡是「必须碰游戏 / 真内存 / 采数 / 评估 / GPU 训练」的步骤
  → 只在设备 B 上执行并验收
```

| 设备 | 路径 / 环境（按实机填写） |
|------|---------------------------|
| 设备 A | 项目 `D:\BossMind`；Python `C:/Users/22930/.conda/envs/BossMind/python.exe`（**已确认 3.12.13**）— 写代码/无 HK 单测 |
| 设备 B | OS：**Windows 10/11**；GPU：**RX 7900 XT**；项目 `E:\BossMind`；Python `C:/Users/22930/.conda/envs/BossMind/python.exe`（**3.12.13**）；WSL 训练见 **§6.1** |

**同步原则**：源码与 `AGENTS.md` 走 Git，两边都 pull 再写、写完就 push。`data/`、`artifacts/ckpt/` 默认留在设备 B（或 LFS/网盘）；设备 A 一般不存大体积轨迹/权重。

---

## 2. 当前状态（每轮必改）

| 字段 | 值 |
|------|-----|
| 当前阶段 | **Phase 0 — 真环境探针** |
| 当前子课 | **第 3 课：按键注入冒烟（probe_input）** |
| 完成度 | 第 1 课 B 机已通过；第 2 课 A 机代码就绪，**B 机验收待补**；第 3 课进行中 |
| 阻塞 / 风险 | 第 2 课未 B 验收前，偏移是否正确未知；第 3 课不依赖 HP 读数，可并行开发 |
| 活跃设备备注 | 设备 A 开发第 3 课；B 机后续补第 2 课验收 |
| 最后更新 | 2026-07-23 |

### 完成清单（勾选）

**双端开发（A 与 B）**

- [ ] Git 远程已配置；交替开发前先 `pull`，结束后 `push` 并更新本文件
- [ ] 不把「仅在 A 上跑通」当作游戏/训练类任务的完成标准

**设备 B — Windows 游戏 / 探针栈（Phase 0 运行验收地）**

- [x] Win10/11 + 管理员权限可用（B 机 `probe_attach` 已验收）
- [x] Steam 空洞骑士安装，版本锁定（关自动更新），进程名已记入 `configs/game_version.yaml`
- [x] Conda/venv：**Python 3.12** + `pip install -r requirements.txt`（A/B 均已装，2026-07-21）
- [x] Cursor 工作区 Python 解释器 / Ruff / YAML 插件（B 机，2026-07-21）
- [x] `probe_attach.py` 附加逻辑（A 机 PyCharm 冒烟；**B 机 HK 正式验收通过**，2026-07-21）
- [x] Cheat Engine 7.7 已安装（B 机；Windows 用 `CheatEngine77.exe` 或 Patreon 版 `CheatEngine77P.exe`）
- [ ] 读 HP — A 机代码就绪，**B 机验收待补**
- [ ] 按键注入冒烟（`probe_input.py`）— **当前**
- [ ] 重置×10 / `results/phase0.md`

**设备 B — GPU 训练栈（可与 Phase 0 并行安装，训练待 Phase 1）**

- [ ] Adrenalin（文档指定的 WSL2 版本）已装并重启
- [ ] WSL2 + Ubuntu 22.04 或 24.04
- [ ] ROCm + PyTorch（ROCm wheel）冒烟通过（见 §6.1）
- [ ] 项目路径在 WSL 可访问（如 `/mnt/e/BossMind`）；训练热数据用 ext4 缓存（§6.1）

**Phase 1+**（未开始）

- [ ] 专家轨迹采集（B · Windows）
- [ ] BC 训练（B · WSL2+ROCm）
- [ ] 固定存档评估（B · Windows）
- [ ] Option / LLM / 训练师 / 消融 …

---

## 3. 下一步

### 第 3 课：按键注入冒烟（当前）

**目标**：脚本能让游戏角色执行一组预设按键（如右走 1 秒 → 跳 → 攻击），人眼可见。

| 设备 | 做什么 |
|------|--------|
| **A** | 写 `src/bossmind/env_tools/input.py` + `scripts/probe_input.py`；动作枚举与 yaml 可配置（可选） |
| **B** | 开 HK、窗口在前台 → 跑 `probe_input` 验收；与第 2 课 `probe_hp` 验收可同次完成 |

**验收（B 机）**

```text
python scripts\probe_input.py
# 期望：角色明显移动/跳跃/攻击；脚本结束无异常
```

**本课不做**：读档重置、BC、复杂连招。

**B 机待补**：第 2 课 `probe_hp` 验收（见 §3 附录）。

### §3 附录 — 第 2 课 B 机验收（待补）

```text
python scripts\probe_attach.py
python scripts\probe_hp.py
```

---

## 4. 阶段地图（勿跳关）

```text
代码编写     → 设备 A 或 B 交替（Git 同步）
Phase 0 运行验收 → 仅设备 B · Windows 原生
Phase 1 采集/评估 → 仅设备 B · Windows；BC 训练 → 设备 B · WSL2+ROCm
Phase 2–5 逻辑 → A 或 B 都可写；凡需 HK/GPU 的跑通与出数 → 在 B
```

可选：CNN / VLM / RAG / 轻 RL — 训练在 B·WSL，采集在 B·Windows。

---

## 5. 仓库结构（当前）

```text
BossMind\
  AGENTS.md
  pyproject.toml
  requirements.txt
  configs\game_version.yaml
  scripts\
    probe_attach.py
    probe_hp.py
    probe_input.py            # 第 3 课（待建）
  src\bossmind\
    paths.py
    env_tools\
      memory.py
      input.py                # 第 3 课（待建）
  data\  artifacts\  results\
```

**安装**：`pip install -e .`

---

| 场景 | 哪里跑 | 栈 |
|------|--------|-----|
| 内存读 / 按键 / 存档 / 采集 / 局内推理 | 设备 B · **Windows 原生 Python** | pymem、pydantic、pyyaml、pydirectinput… |
| BC / CNN / 可选 RL 训练 | 设备 B · **WSL2 + ROCm + PyTorch** | 见 §6.1（宿主仍是 Windows） |
| 业务逻辑编写 | 设备 A 或 B（交替） | 编辑器 + Git；A 可不装全套 pymem/HK |
| LLM API | 任意设备发起；局内服务建议在 B | OpenAI 兼容 Function Calling |

原则：偏移进 YAML；实时进程与训练进程隔离；Gate 通过才发布策略版本；**不在战斗进程内热更新权重**。

---

## 6.1 设备 B 环境配置方案（Windows 强制 · 详细可用）

> **约束**：设备 B 必须保持 **Windows** 作为宿主（空洞骑士 + `pymem` 只能稳妥跑在 Windows）。  
> **GPU**：RX 7900 XT → 训练走 **同机 WSL2 内的 ROCm**，不是 Linux 双系统必选项，也不是 CUDA。

### 主力机共存约束（设备 B 很重要）

设备 B 是用户 **日常主力机**（还会玩其他游戏）。配置与使用必须服从：

| 原则 | 做法 |
|------|------|
| 训练时再开算力 | **不玩游戏时**再开 WSL 训练；训练期间不要 3A/竞技开黑 |
| 驱动求稳不求日更 | Adrenalin 可锁在 ROCm 文档指定版本，**关自动更新**；若某新游强依赖新驱动，再评估「临时升驱动 vs 训练环境重装」 |
| 工具按需启动 | `pymem`/注入脚本只在跑 BossMind 时开；打网游、反作弊游戏前关掉探针 |
| 资源别常驻 | 不用时 `wsl --shutdown`，避免后台占内存/偶发占 GPU |
| 先游戏栈、后训练栈 | Phase 0 可只装 Windows 侧 pymem；**WSL+ROCm 等到要训 BC 再装**，减少早期对日常的扰动 |

**预期影响（诚实）：** 正常上网/办公/多数单机游戏 ≈ 无感；同时「重度训练 + 玩游戏」会抢 GPU/卡顿；锁驱动可能让你拿不到最新游戏优化；极少数反作弊对读内存类工具敏感（BossMind 工具运行时避开即可）。

---


```text
┌──────────────────────── 设备 B = Windows 11/10 ────────────────────────┐
│                                                                        │
│  【栈 1 · 游戏运行时】Windows 原生                                      │
│    Steam HK · conda/venv Python3.12 · pymem · 按键 · 采集 · 评估         │
│    写 data/raw/ · 读 artifacts/published/                              │
│                                                                        │
│  【栈 2 · GPU 训练】WSL2 Ubuntu · ext4 训练缓存                          │
│    ROCm · PyTorch · 训练只读 ~/bossmind-train/data/                    │
│    临时 ckpt/logs 在 ~/bossmind-train/artifacts/runs/                  │
│    仅 best.ckpt 回传 Windows artifacts/published/                      │
│                                                                        │
│  7900 XT ← Adrenalin 驱动同时服务：游戏画面 + WSL 计算                   │
└────────────────────────────────────────────────────────────────────────┘
```

游戏 **不要** 放进 WSL；训练 **不要** 指望 Windows 原生 CUDA（没有 NVIDIA）。

### 训练数据流（性能约束 — 必读）

**问题**：`/mnt/d` 是 Windows NTFS 挂载，跨 WSL 边界 I/O 慢，尤其小文件、`stat`、DataLoader 多 worker 随机读；**不是数据会丢，而是每个 epoch 重复付跨边界开销**。

**推荐方案**：`Windows 采集源 + WSL ext4 训练缓存 + 发布回 Windows`

| 位置 | 放什么 |
|------|--------|
| `D:\BossMind\data\raw\` | Windows 采集的轨迹/JSONL（源数据） |
| `D:\BossMind\artifacts\published\<run_id>\` | 训练后**发布**的 ckpt + `metadata.json`（Windows 评估只读这里） |
| `D:\BossMind\results\` | 评估报告 |
| `~/bossmind-train/data/`（WSL ext4） | 增量同步后的训练热数据 |
| `~/bossmind-train/artifacts/runs/`（WSL ext4） | 训练日志、临时 checkpoint、缓存 |

**不要用符号链接指向 `/mnt/d` 当性能优化** — 仍走跨边界，且权限更麻烦。

| 方案 | 适用 |
|------|------|
| 全在 `/mnt/d/BossMind` 训练 | Phase 0 / 极小数据冒烟 |
| **ext4 缓存 + 增量同步**（推荐） | 正式 BC/CNN 多 epoch |
| 仅同步 `data/` 到 ext4，代码仍 `/mnt/d` | 可接受的简化版 |

**采集 manifest**：每批 Windows 采集后写 `data/raw/<batch_id>/manifest.json`（样本数、时间、数据版本）；WSL 只同步 manifest 里**新增**的 batch。

---

## 6.2 最终训练输入：内存 + CNN 最优配置（必读）

> 一句话：**内存高频管操作，图像低频管招式语义；训练时先独立训 CNN、再冻结并预计算特征，最后训 BC。**  
> 不是「每帧内存 + 每帧整图」端到端硬训。

### 6.2.1 两条数据流（采集在 Windows）

| 流 | 频率 | 存什么 | 用途 |
|----|------|--------|------|
| **内存/动作流** | 60–120 Hz | HP、位置、速度、Boss 状态、**实际发出的按键** | 高频控制、精确时序 |
| **ROI 图像流** | 10–20 Hz | 固定区域截图（Boss 战画面） | 招式/阶段/威胁语义 |

**对齐规则（防泄漏）**：

- 时间用同一进程的 `perf_counter_ns()`，不用墙钟  
- 每个决策样本只关联 **`image_t_ns <= decision_t_ns` 的最近一张图**  
- 记录 `image_age_ms`；过期图（如 >100ms）不进视觉 BC 或显式标 stale  
- **不要**为每条内存记录各存一张图；一张 15Hz 图可被多个内存样本引用  

**一条训练样本（概念）**：

```text
mem_vector + action_label + decision_t_ns
+ frame_id + image_t_ns + image_age_ms + episode_id
```

Windows 每局落盘建议：

```text
data/raw/<batch_id>/<episode_id>/
  events.jsonl          # 高频原始流（采集中先写，防崩溃）
  frames.parquet        # frame_id, t_ns, roi_id, 图片路径
  images/battle_v1/     # 000000351.jpg ...
  episode_meta.json
  samples.parquet       # 后处理：因果对齐后的训练索引
```

### 6.2.2 CNN 的两个角色（勿混淆）

| 角色 | 何时 | 在哪跑 | 输入→输出 |
|------|------|--------|-----------|
| **A. 离线训 CNN** | Phase 2 | WSL ext4 | ROI 图 → 招式分类器 + **encoder** |
| **B. 在线视觉推理** | 局内 play | Windows | ROI 图 → **embedding + move_probs**（+ 调试用 move_id） |

正式 BC **推荐输入**（不是端到端原图）：

```text
[mem_vector, cnn_embedding, move_probs, image_age_ms]
```

- 不只拼硬 `move_id`：分类错一次信息全丢；embedding + 软概率更稳  
- 默认 **不** 用 `Policy(mem, raw_image)` 端到端：难调、慢、分不清是 CNN 错还是策略错  

### 6.2.3 三档配置策略（按阶段选用）

| 档位 | 输入 | CNN | 数据放哪 | 通过标准 |
|------|------|-----|----------|----------|
| **Phase 1 纯内存 BC** | 仅 `mem_vector` + 动作 | 不训或只存诊断图 | Windows raw → WSL 同步 mem 样本 | 对齐无错、基础操作可复现 |
| **Phase 2 +CNN** | 内存 + 10–20Hz ROI | **独立训 CNN 并冻结** | ROI 图 **必须** 复制到 WSL ext4 | CNN 按 episode 验证通过；加视觉后优于纯内存 |
| **正式训练** | mem + embedding + move_probs + image_age | 固定 `vision_id`，**预计算特征** | BC 只读 `features/<vision_id>/`，**不再读原图** | 固定存档多局达标；完整包可在 Windows 独立加载 |

**关键**：CNN 权重 / ROI / 归一化 / 标签顺序任一变更 → 新 `vision_id` → **必须重算特征**，不得混用旧特征。

### 6.2.4 完整流水线（逐步：在哪跑、读哪、写哪）

```text
① 采集          Windows    HK + 内存 + 按键 + ROI 截图
                 写 → D:\BossMind\data\raw\<batch_id>\ + manifest.json

② 后处理对齐    Windows 或 WSL   因果关联图与决策时刻，过滤无效样本
                 写 → data/processed/<dataset_id>/samples.parquet

③ 同步          WSL        仅增量同步新 batch → ~/bossmind-train/data/raw_mirror/
                 ⚠ 训练 DataLoader 不长期读 /mnt/d

④ 训 CNN        WSL ext4   读 ext4 上的 ROI 图 + 标签
                 写 → ~/bossmind-train/artifacts/runs/cnn_<run_id>/
                 发布 → D:\BossMind\artifacts\published\vision_<vision_id>\

⑤ 预计算特征    WSL ext4   用锁定 CNN 对每条 BC 样本写 embedding/probs
                 写 → ~/bossmind-train/data/features/<dataset_id>/<vision_id>/

⑥ 训 BC         WSL ext4   只读 mem + 预计算特征 + image_age
                 写 → ~/bossmind-train/artifacts/runs/bc_<run_id>/

⑦ 发布          WSL→Windows  策略 + 视觉模型 + ROI 配置 + 归一化 + metadata
                 写 → D:\BossMind\artifacts\published\<run_id>\

⑧ 评估          Windows    只读 published 包，固定存档 eval
                 写 → D:\BossMind\results\
```

**发布包必须含**：策略权重、视觉 encoder、ROI 配置、输入归一化、标签表、动作映射、`dataset_id`、`vision_id`、Git commit。Windows 评估 **禁止** 读 WSL 临时 ckpt。

### 6.2.5 DataLoader 要点

| 训练对象 | 数据位置 | workers | 其它 |
|----------|----------|---------|------|
| CNN | WSL ext4 图像（大分片优于海量小文件） | 4 起测 | 增广仅 train；按 **episode** 切分 train/val |
| BC（冻结 CNN 后） | ext4 预计算特征 `.npz`/`.pt` 分片 | 2–4 | **不读原图**；batch 跨 episode 随机 |

- train/val/test **按 episode 切**，禁止随机拆相邻帧（会泄漏）  
- `pin_memory` 在 ROCm 下需实测，有提升才开  

### 6.2.6 和 §6.1 跨边界 I/O 的关系

```text
Windows data/raw     = 永久源数据（内存轨迹 + ROI 图）
WSL ext4             = 训练热数据（图副本 + 预计算特征）
跨边界传输           = 采集后同步一次 + 训练后发布 ckpt 一次
每个 epoch           = 只读 ext4，不扫 /mnt/d
```

---

### 栈 1 — Windows 游戏 / 探针 / 采集（Phase 0 立刻需要）

1. **系统**  
   - Windows 10/11 64-bit；开发时对读内存脚本使用「以管理员身份运行」终端（按需）。  

2. **显卡驱动（游戏 + 为栈 2 打底）**  
   - 安装 AMD 文档要求的 **Adrenalin Edition for WSL2**（版本号以 [AMD ROCm on Radeon WSL](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/) 当前页为准，例如文档写的 26.x）。  
   - 装完 **重启**。  
   - 建议关闭驱动自动更新，避免 ROCm 组合被静默升级弄挂。  

3. **游戏**  
   - Steam 安装 Hollow Knight；**锁定版本 / 关自动更新**。  
   - 任务管理器确认进程名（常见 `hollow_knight.exe`，以实机为准）写入 `configs/game_version.yaml`。  
   - 准备 Boss 前手动存档，供后续重置协议使用。  

4. **Python（Windows）**  
   - **Python 3.12**：`conda create -n BossMind python=3.12`  
   - `pip install -r requirements.txt`  
   - **不要**在 Windows env 装 CUDA 版 PyTorch；WSL 训 BC 时再按文件头注释装 ROCm torch。  

5. **Phase 0 验收命令（在 B 的 Windows 终端）**  

```text
conda activate BossMind
cd /d D:\BossMind
python scripts\probe_attach.py
```

开着 HK 应打印 PID；关掉应清晰失败。

---

### 栈 2 — 同机 WSL2 + ROCm 训练（Phase 1 前装好冒烟即可）

> 宿主仍是 Windows，满足「设备 B 强制 Windows」；GPU 训练在 WSL 用户态完成。7900 XT 在 AMD WSL 支持列表中。

1. **启用 WSL2**（管理员 PowerShell）：  

```powershell
wsl --install
# 或确保：wsl --set-default-version 2
```

安装 **Ubuntu 22.04 或 24.04**（与当前 AMD 文档一致）。重启如有提示则重启。

2. **在 WSL 内安装 ROCm**  
   - 严格按 AMD 当前文档「Install Radeon software for WSL with ROCm」操作（usecase / librocdxg 以官网为准）。  
   - 关键点：WSL 场景常用 `--no-dkms`；不要混装乱七八糟的 amdgpu 教程。  

3. **在 WSL 内安装 PyTorch（ROCm 轮）**  
   - 版本组合以 AMD「PyTorch for Radeon on WSL」页为准。示例（**版本号请核对后替换**）：  

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm7.2
```

4. **冒烟（WSL）**  

```bash
python -c "import torch; print('ok', torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
```

期望：`True`，名称含 7900 XT 或 gfx1100 一类。  
说明：ROCm 上 PyTorch 仍使用 `torch.cuda.*` API 命名。

5. **访问代码与训练缓存（不要从 `/mnt/d` 直接训练热数据）**  

```bash
# 代码可从 /mnt/d 拉取或 git clone 到 WSL home
cd /mnt/d/BossMind          # 只读代码、看配置
# 训练数据与 ckpt 在 ext4：
mkdir -p ~/bossmind-train/{data,artifacts/runs}
```

训练脚本 `--data-dir ~/bossmind-train/data`；**不要**让 DataLoader 每个 epoch 扫 `/mnt/d/.../data`。

6. **依赖**  
   - 统一：`requirements.txt`（功能分区注释）  
   - WSL 另装 ROCm 版 `torch`（见 requirements 文件头）  
   - 设备 A 写代码为主，通常不必装 ROCm / 全套游戏依赖  

---

### 备选（仅当 WSL+ROCm 长期失败）

| 方案 | 说明 |
|------|------|
| 原生 Linux 双系统 + ROCm | 训练往往更稳，但打破「日常只用 Windows」习惯；游戏采集仍建议回 Windows |
| Windows `torch-directml` | 可原生 Windows 训练，生态与示例弱于 ROCm，作临时退路 |

**避免**：ZLUDA、在 Windows 强行装 NVIDIA CUDA 版 torch。

---

### 日常工作流（交替开发 + 训练 I/O）

```text
【写代码】设备 A 或 B
  pull → 改代码/文档 → 更新 AGENTS.md → commit → push

【采集】仅设备 B · Windows
  pull → 开 HK → 采集写 D:\BossMind\data\raw\<batch_id>\
  → 写 manifest.json（样本数、版本、时间）

【训练】仅设备 B · WSL2+ROCm
  1) 从 /mnt/d/BossMind 或 git 对齐代码
  2) 增量同步新 batch → ~/bossmind-train/data/（rsync 或自写 sync 脚本）
  3) 训练只读 ext4；日志/临时 ckpt → ~/bossmind-train/artifacts/runs/
  4) 选 best.ckpt + metadata.json → 复制到 D:\BossMind\artifacts\published\<run_id>\

【评估】仅设备 B · Windows
  只读 artifacts\published\ 下已发布权重 → 固定存档 eval → results\
```

**原则**：跨边界传数据**集中在训练前后各一次**（同步进 ext4、发布 ckpt 回 Windows），不要每个 epoch 走 `/mnt/d`。

---

## 7. 协作约定（用户 ↔ Agent）

| Agent 应做 | Agent 不应做 |
|------------|--------------|
| 先读分工：A/B **都能写代码**；仅 B 能验收游戏与 GPU 训练 | 要求在设备 A 上完成 Phase 0 游戏/训练正式验收 |
| 讲思路、审代码、排错 | 未要求时代写整模块完工代码 |
| 每轮更新本 `AGENTS.md` | 假设另一台有完整聊天记录 |
| 指导 B 的 Windows+WSL 两套环境 | 让用户改用 Linux 作为 B 的唯一系统（除非用户改口） |
| 提醒交替开发先 pull 后 push | 战斗进程内热更新权重 |

换设备开聊建议首句：

> 请先读 `AGENTS.md`。我在设备 A/B（说明哪台）。A/B 交替写代码；游戏与训练验收只在 B。按 §3 下一步继续。

---

## 8. 项目日志（仅里程碑）

> 只记：阶段验收通过/失败、架构定稿、环境冒烟结果、求职向交付物。  
> **不要**记录：文档措辞修改、依赖文件整理、重复澄清分工等。

### 2026-07-23

- Phase 0 **第 2 课 A 机代码就绪**：`PlayerInfo`（attach/detach/指针链/读 HP）+ `probe_attach` + `probe_hp`；待 **B 机正式验收**

### 2026-07-21

- Phase 0 **第 1 课通过**（A 机）：`paths.py` + `env_tools/memory` + 可配置 `probe_attach`
- Phase 0 **第 1 课 B 机正式验收通过**：开 HK 运行 `probe_attach` 可获取 PID
- **设备 B** 环境就绪：`E:\BossMind`、conda 3.12.13、CE 7.7

---

## 9. 交接检查清单（换设备前）

- [ ] §2 / §3 已更新；若有里程碑则更新 §8  
- [ ] 代码已 commit + push  
- [ ] 设备 A/B 路径已填入 §1  
- [ ] 大文件 `data/`、`ckpt/` 在 B 上或有网盘副本  
- [ ] 若动过驱动/ROCm：把冒烟结果写入 §8  
