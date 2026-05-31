{{/*
  Expand the full image name:
  Usage: {{ include "shopcart.image" (dict "registry" .Values.global.registry "repo" .Values.userService.image.repository "tag" .Values.global.imageTag) }}
*/}}
{{- define "shopcart.image" -}}
{{- printf "%s/%s:%s" .registry .repo .tag -}}
{{- end }}

{{/*
  Common labels applied to all resources
*/}}
{{- define "shopcart.labels" -}}
app.kubernetes.io/managed-by: Helm
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
environment: {{ .Values.global.environment }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
{{- end }}