export default function sanitizeFilename(name: string) {
return name.replace(/[^a-z0-9_.-]/gi, '_').toLowerCase();
}