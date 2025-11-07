// Prevents the CS0656 compiler error when building under .NET 6 for IL2CPP
#nullable enable
namespace System.Runtime.CompilerServices
{
    [System.AttributeUsage(System.AttributeTargets.All, Inherited = false)]
    internal sealed class NullableAttribute : System.Attribute
    {
        public NullableAttribute(byte b) { }
        public NullableAttribute(byte[]? b) { }
    }

    [System.AttributeUsage(System.AttributeTargets.Class | System.AttributeTargets.Struct | System.AttributeTargets.Interface, Inherited = false)]
    internal sealed class NullableContextAttribute : System.Attribute
    {
        public NullableContextAttribute(byte b) { }
    }
}
