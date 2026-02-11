"use client"

import * as React from "react"
import * as LabelPrimitive from "@radix-ui/react-label"
import { Slot } from "@radix-ui/react-slot"
import { cn } from "@/lib/utils"

// Simple form context for validation state
interface FormFieldContextValue {
  name: string;
  error?: string;
}

const FormFieldContext = React.createContext<FormFieldContextValue>(
  {} as FormFieldContextValue
)

// Form field component
interface FormFieldProps {
  name: string;
  error?: string;
  children: React.ReactNode;
}

const FormField = ({ name, error, children }: FormFieldProps) => {
  return (
    <FormFieldContext.Provider value={{ name, error }}>
      <div className="space-y-2">{children}</div>
    </FormFieldContext.Provider>
  )
}

// Form label component
const FormLabel = React.forwardRef<
  React.ElementRef<typeof LabelPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof LabelPrimitive.Root>
>(({ className, ...props }, ref) => {
  const { error } = React.useContext(FormFieldContext)

  return (
    <LabelPrimitive.Root
      ref={ref}
      className={cn(
        "text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70",
        error && "text-destructive",
        className
      )}
      {...props}
    />
  )
})
FormLabel.displayName = LabelPrimitive.Root.displayName

// Form control wrapper
const FormControl = React.forwardRef<
  React.ElementRef<typeof Slot>,
  React.ComponentPropsWithoutRef<typeof Slot>
>(({ ...props }, ref) => {
  const { error } = React.useContext(FormFieldContext)

  return (
    <Slot
      ref={ref}
      aria-invalid={!!error}
      {...props}
    />
  )
})
FormControl.displayName = Slot.displayName

// Form description text
const FormDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => {
  return (
    <p
      ref={ref}
      className={cn("text-sm text-muted-foreground", className)}
      {...props}
    />
  )
})
FormDescription.displayName = "FormDescription"

// Form error message
const FormMessage = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, children, ...props }, ref) => {
  const { error } = React.useContext(FormFieldContext)

  if (!error && !children) {
    return null
  }

  return (
    <p
      ref={ref}
      className={cn("text-sm font-medium text-destructive", className)}
      {...props}
    >
      {error || children}
    </p>
  )
})
FormMessage.displayName = "FormMessage"

// Simple form component
interface FormProps extends React.FormHTMLAttributes<HTMLFormElement> {
  children: React.ReactNode;
}

const Form = React.forwardRef<HTMLFormElement, FormProps>(
  ({ className, children, ...props }, ref) => {
    return (
      <form ref={ref} className={cn("space-y-6", className)} {...props}>
        {children}
      </form>
    )
  }
)
Form.displayName = "Form"

// Label component
const Label = React.forwardRef<
  React.ElementRef<typeof LabelPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof LabelPrimitive.Root>
>(({ className, ...props }, ref) => (
  <LabelPrimitive.Root
    ref={ref}
    className={cn(
      "text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70",
      className
    )}
    {...props}
  />
))
Label.displayName = LabelPrimitive.Root.displayName

export {
  Form,
  FormField,
  FormLabel,
  FormControl,
  FormDescription,
  FormMessage,
  Label,
}
