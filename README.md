# PilotEdge Audio Fetcher

This service periodically downloads PilotEdge audio recordings and stores them on persistent storage so they can be consumed by media applications (e.g. Jellyfin).

It is designed to run as a Kubernetes CronJob and is deployed via Helm and Argo CD.

---

## What this does

- Runs once per day as a Kubernetes CronJob
- Downloads PilotEdge audio recordings
- Stores audio files in a persistent volume
- Exposes no services or ports

The fetcher **owns the audio data lifecycle**. Other applications are expected to consume the files read-only.

---

## Architecture

- **Namespace:** <same namespace as consumer>
- **Workload:** Kubernetes `CronJob`
- **Storage:** PersistentVolumeClaim (`pvc-pe-audio`)
- **Deployment:** Helm chart, reconciled by Argo CD

Audio files are written to:

/media/pe/YYYY-MM-DD/

---

## Data ownership

This application is the **producer** of PilotEdge audio and therefore owns:

- Directory structure
- Retention policy
- PVC definition and sizing

Consumers (e.g. Jellyfin) mount the PVC but do not manage it.

---

## Configuration

All configuration is done via Helm values.

Key values include:

- Cron schedule
- PVC size
- StorageClass

See `values.yaml` for defaults.

---

## Deployment (GitOps)

This chart is intended to be deployed via Argo CD.

The Argo CD `Application` manifest lives in the `home-gitops` repository and points at:

helm/pilotedge-audio-fetcher

Manual `helm install` is supported for local testing.

---

## Notes

- This service assumes single-node access to the PVC (ReadWriteOnce)
- Designed for homelab / personal use
- Not intended for high availability or multi-writer setups
