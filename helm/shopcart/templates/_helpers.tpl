{{/*
  Builds full image URL:
  shopcartacr.azurecr.io/user-service:42

  Called like:
  {{ include "shopcart.image" (dict "root" . "repo" .Values.userService.image.repository) }}
*/}}
{{- define "shopcart.image" -}}
{{- $registry := .root.Values.global.registry -}}
{{- $tag      := .root.Values.global.imageTag -}}
{{- $repo     := .repo -}}
{{- if not $registry -}}
  {{- fail "global.registry must be set. Pass --set global.registry=<ACR_URL> from pipeline." -}}
{{- end -}}
{{- if not $tag -}}
  {{- fail "global.imageTag must be set. Pass --set global.imageTag=<BUILD_ID> from pipeline." -}}
{{- end -}}
{{- printf "%s/%s:%s" $registry $repo $tag -}}
{{- end }}