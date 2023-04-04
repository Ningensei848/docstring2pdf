

- `overrides/` はトラッキングしないようにしてあるので注意 (at .gitignore)


### Workload Identity 下準備　メモ


```
# TODO(developer): Update this value to your GitHub repository.
export REPO="Ningensei848/docstring2pdf"

export PROJECT_ID="q4rs-project"
export POOL_NAME="pool-for-actions"
export PROVIDER_NAME="provider-for-actions"
```

### サービスアカウントを作成する

```
gcloud iam service-accounts create "my-service-account" \
  --project "${PROJECT_ID}"
```

### APIを有効化する

```
gcloud services enable iamcredentials.googleapis.com \
  --project "${PROJECT_ID}"
```

### プールの作成：


```
gcloud iam workload-identity-pools create "${POOL_NAME}" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --display-name="Pool for GitHub Actions"
```

#### Workload Identity の ID を得る

```
gcloud iam workload-identity-pools describe "${POOL_NAME}" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --format="value(name)"
```

→　projects/137544258857/locations/global/workloadIdentityPools/pool-for-actions

勝手にプロジェクト名に変えてはダメ（１敗）

> Note that $WORKLOAD_IDENTITY_POOL_ID should be the full Workload Identity Pool resource ID, like:
> `projects/123456789/locations/global/workloadIdentityPools/my-pool`

### 環境変数に保存しておく


```
export WORKLOAD_IDENTITY_POOL_ID="projects/137544258857/locations/global/workloadIdentityPools/${POOL_NAME}"

echo $WORKLOAD_IDENTITY_POOL_ID
```

#### そのプールのプロバイダを作成

```
gcloud iam workload-identity-pools providers create-oidc "${PROVIDER_NAME}" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="${POOL_NAME}" \
  --display-name="Provider for GitHub Actions" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
  --issuer-uri="https://token.actions.githubusercontent.com"
```

### サービスアカウントに対してロールを与える

```
gcloud iam service-accounts add-iam-policy-binding "rclone@${PROJECT_ID}.iam.gserviceaccount.com" \
  --project="${PROJECT_ID}" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/${REPO}"
```

特定リポジトリだけでなく、GitHub 全体に触れさせたい時：
```
--member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository_owner/${OWNER}"
```

### Workload Identity のプロバイダ名を取得してみる

```
gcloud iam workload-identity-pools providers describe "${PROVIDER_NAME}" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="${POOL_NAME}" \
  --format="value(name)"
```

→　projects/137544258857/locations/global/workloadIdentityPools/pool-for-actions/providers/provider-for-actions

作成できているようだ