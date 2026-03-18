export default function LoadingSpinner() {
    return (
        <div className="min-h-screen bg-gray-950 flex items-center justify-center">
            <div className="text-center">
                <div className="relative w-20 h-20 mx-auto mb-4">
                    <div className="absolute inset-0 border-4 border-gray-800 rounded-full"></div>
                    <div className="absolute inset-0 border-4 border-cyan-500 rounded-full border-t-transparent animate-spin"></div>
                </div>
                <p className="text-gray-400 text-sm font-mono">Initializing SecureSight...</p>
            </div>
        </div>
    );
}
