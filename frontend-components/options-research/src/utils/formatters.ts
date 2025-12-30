/**
 * Financial formatting utilities for the Options Research Suite
 */

/**
 * Format a number as currency
 */
export function formatCurrency(value: number | null, decimals = 2): string {
  if (value === null) return "N/A";
  return `$${value.toFixed(decimals)}`;
}

/**
 * Format a number as percentage
 */
export function formatPercent(value: number | null, decimals = 1): string {
  if (value === null) return "N/A";
  // Handle values that might be decimals (0.35) or already percentages (35)
  const pct = value > 1 ? value : value * 100;
  return `${pct.toFixed(decimals)}%`;
}

/**
 * Format a date string for display
 */
export function formatDate(dateStr: string | null): string {
  if (!dateStr) return "N/A";
  try {
    const date = new Date(dateStr);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  } catch {
    return dateStr;
  }
}

/**
 * Format relative time (e.g., "5 days")
 */
export function formatRelativeTime(days: number | null): string {
  if (days === null) return "N/A";
  if (days === 0) return "Today";
  if (days === 1) return "Tomorrow";
  if (days < 0) return `${Math.abs(days)} days ago`;
  return `${days} days`;
}

/**
 * Format IV environment for display
 */
export function formatIVEnvironment(
  env: "very_low" | "low" | "neutral" | "elevated" | "very_high" | string
): string {
  const labels: Record<string, string> = {
    very_low: "Very Cheap",
    low: "Cheap",
    neutral: "Average",
    elevated: "Expensive",
    very_high: "Very Expensive",
  };
  return labels[env] || env.replace("_", " ");
}

/**
 * Format strategy name for display
 */
export function formatStrategyName(strategy: string): string {
  return strategy
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

/**
 * Get color class for IV environment
 */
export function getIVEnvironmentColor(
  env: "very_low" | "low" | "neutral" | "elevated" | "very_high" | string
): string {
  const colors: Record<string, string> = {
    very_low: "text-green-400",
    low: "text-lime-400",
    neutral: "text-yellow-400",
    elevated: "text-orange-400",
    very_high: "text-red-400",
  };
  return colors[env] || "text-grey-400";
}
