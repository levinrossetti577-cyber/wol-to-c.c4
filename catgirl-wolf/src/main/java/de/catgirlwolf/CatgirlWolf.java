package de.catgirlwolf;

import net.fabricmc.api.ModInitializer;
import net.minecraft.world.entity.EntityDimensions;
import net.minecraft.world.entity.animal.wolf.Wolf;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Gemeinsamer Einstiegspunkt (Client und Server).
 * Die Mod verändert keine Wolfslogik. Einzige serverseitige Änderung ist die
 * spielergroße Hitbox (siehe {@link de.catgirlwolf.mixin.LivingEntityDimensionsMixin}).
 */
public class CatgirlWolf implements ModInitializer {
	public static final String MOD_ID = "catgirlwolf";
	public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	/** Spielermaße: 0,6 x 1,8 Blöcke, Augenhöhe 1,62. Babys werden wie in Vanilla halbiert. */
	private static final EntityDimensions CATGIRL = EntityDimensions.scalable(0.6F, 1.8F).withEyeHeight(1.62F);

	public static EntityDimensions dimensionsFor(Wolf wolf) {
		return CATGIRL.scale(wolf.getAgeScale());
	}

	@Override
	public void onInitialize() {
		LOGGER.info("Catgirl Wolf geladen: Wölfe erhalten Spielergröße.");
	}
}
