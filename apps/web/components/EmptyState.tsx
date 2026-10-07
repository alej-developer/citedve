export function EmptyState({ message = "No se encontraron datos para este período." }: { message?: string }) {
  return (
    <div className="py-12 px-6 border border-dashed border-rule text-center bg-paper-raised">
      <p className="font-serif text-lg text-ink-soft">{message}</p>
      <p className="mt-2 text-sm text-ink-soft opacity-80 max-w-md mx-auto">
        Mantenemos un rigor estricto: ninguna cifra se publica sin su fuente verificable.
      </p>
    </div>
  );
}
