export default function Empty({ text='Chưa có dữ liệu' }: { text?: string }) {
  return <div className="card p-6 text-center text-gray-500">{text}</div>
}
