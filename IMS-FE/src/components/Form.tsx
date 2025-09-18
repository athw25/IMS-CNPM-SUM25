import { clsx } from 'clsx'

export function Input({label, ...rest}: any) {
  return (
    <label className="block">
      <div className="label">{label}</div>
      <input {...rest} className={clsx('input', rest.className)} />
    </label>
  )
}
export function Select({label, children, ...rest}: any) {
  return (
    <label className="block">
      <div className="label">{label}</div>
      <select {...rest} className={clsx('input', rest.className)}>{children}</select>
    </label>
  )
}
export function Textarea({label, ...rest}: any) {
  return (
    <label className="block">
      <div className="label">{label}</div>
      <textarea {...rest} className={clsx('input', rest.className)} />
    </label>
  )
}
export function DateTime({label, ...rest}: any) {
  return <Input type="datetime-local" label={label} {...rest} />
}
export function Actions({children}: {children: React.ReactNode}) {
  return <div className="flex items-center gap-2">{children}</div>
}
