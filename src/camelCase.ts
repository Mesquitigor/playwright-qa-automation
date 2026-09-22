/**
 * Converts a string into camelCase.
 *
 * Words are separated by any non-letter delimiter. The first word is
 * lowercased; every following word is capitalized. Delimiters are removed.
 *
 * @example
 * camelCase("BOB loves-coding") // "bobLovesCoding"
 * camelCase("cats AND*Dogs-are Awesome") // "catsAndDogsAreAwesome"
 * camelCase("a b c d-e-f%g") // "aBCDEFG"
 */
export function camelCase(str: string): string {
  return str
    .split(/[^a-zA-Z]+/)
    .filter(Boolean)
    .map((word, index) => {
      const lower = word.toLowerCase();
      if (index === 0) {
        return lower;
      }
      return lower.charAt(0).toUpperCase() + lower.slice(1);
    })
    .join('');
}
