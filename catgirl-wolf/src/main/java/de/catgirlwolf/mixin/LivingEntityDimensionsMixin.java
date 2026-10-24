package de.catgirlwolf.mixin;

import de.catgirlwolf.CatgirlWolf;
import net.minecraft.world.entity.EntityDimensions;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Pose;
import net.minecraft.world.entity.animal.wolf.Wolf;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Gibt Wölfen eine spielergroße Hitbox, damit das spielergroße Modell nicht in Decken
 * und Blöcken steckt. Wolf selbst überschreibt getDefaultDimensions nicht, deshalb wird
 * in LivingEntity injiziert und auf Wolf geprüft.
 * require = 0: Falls sich die Methode in einer künftigen Version ändert, startet das Spiel
 * trotzdem; dann bleibt nur die Vanilla-Hitbox.
 */
@Mixin(LivingEntity.class)
public abstract class LivingEntityDimensionsMixin {
	@Inject(method = "getDefaultDimensions", at = @At("RETURN"), cancellable = true, require = 0)
	private void catgirlwolf$playerSizedWolf(Pose pose, CallbackInfoReturnable<EntityDimensions> cir) {
		if ((Object) this instanceof Wolf wolf) {
			cir.setReturnValue(CatgirlWolf.dimensionsFor(wolf));
		}
	}
}
