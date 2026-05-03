const STEPS = [
  { key: 'uploading',    label: 'Uploading'    },
  { key: 'extracting',   label: 'Extracting'   },
  { key: 'transcribing', label: 'Transcribing' },
  { key: 'translating',  label: 'Translating'  },
  { key: 'done',         label: 'Done'         },
]

const ORDER = Object.fromEntries(STEPS.map((s, i) => [s.key, i]))

export default function ProgressStepper({ step, message }) {
  const currentIdx = ORDER[step] ?? 0
  const isError = step === 'error'

  return (
    <div className="w-full max-w-lg mx-auto mt-8">
      <ol className="flex items-center w-full mb-4">
        {STEPS.map((s, i) => {
          const done = currentIdx > i
          const active = currentIdx === i && !isError
          return (
            <li key={s.key} className={`flex items-center ${i < STEPS.length - 1 ? 'flex-1' : ''}`}>
              <div className="flex flex-col items-center">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold border-2 transition-all duration-300
                    ${done  ? 'bg-red-700 border-red-600 text-white' : ''}
                    ${active ? 'bg-orange-950 border-orange-400 text-orange-200 chakra-active' : ''}
                    ${!done && !active ? 'bg-[#1a1208] border-orange-950 text-amber-900' : ''}
                  `}
                >
                  {done ? '✓' : i + 1}
                </div>
                <span className={`mt-1 text-xs font-medium
                  ${active ? 'text-orange-400' : done ? 'text-red-500' : 'text-amber-900'}`}>
                  {s.label}
                </span>
              </div>
              {i < STEPS.length - 1 && (
                <div className={`flex-1 h-0.5 mx-2 mb-4 transition-all duration-500
                  ${done ? 'bg-gradient-to-r from-red-700 to-orange-600' : 'bg-orange-950'}`} />
              )}
            </li>
          )
        })}
      </ol>

      <p className={`text-center text-sm mt-2 ${isError ? 'text-red-400' : 'text-amber-700'}`}>
        {isError ? `⚠ Error: ${message}` : message}
      </p>
    </div>
  )
}
